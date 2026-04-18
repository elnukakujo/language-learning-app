import json
import logging
from typing import Optional

from sqlalchemy.orm import Session

from ..core.database import db_manager
from ..utils import text_gen_model, text_gen_tokenizer
from .features import ExerciseService

logger = logging.getLogger(__name__)

exercise_service = ExerciseService()


class FeedbackService:
	tokenizer = text_gen_tokenizer
	model = text_gen_model

	feedback_instruct = (
		"You are a supportive language-learning tutor. "
		"Write short, concrete feedback for a learner after an exercise has been evaluated. "
		"Use at most 2 sentences. Mention one strength, one improvement point, and keep the tone encouraging. "
		"Do not mention internal model details or numerical scoring unless it helps the learner understand the result."
		"Higher similarity, grammar error rate, and token difference means better performance. You can use these metrics to identify specific strengths and weaknesses in the learner's answer compared to the reference answer based on the question asked and metrics."
		"Don't give the correct answer, just feedback on the user's answer and how to improve it."
	)

	feedback_shots = [
		[
			"Exercise type: translate\nScore: 0.92\nCorrect: true\nQuestion: I went to the market.\nUser answer: Je suis allé au marché.\nReference answer: Je suis allé au marché.\nMetrics: {\"similarity\": 0.95, \"grammar_error_rate\": 1.0, \"token_difference_rate\": 1.0}",
			"Good work. Your answer is accurate and natural. If you want to improve further, focus on keeping the sentence equally smooth in different tenses.",
		],
		[
			"Exercise type: speaking\nScore: 0.58\nCorrect: false\nQuestion: 吗\nUser answer: 马\nReference answer: 吗\nMetrics: {\"similarity\": 0.61, \"grammar_error_rate\": 0.82, \"token_difference_rate\": 0.55}",
			"You are on the right track, but the pronunciation still needs work. Listen to the reference again and focus on rhythm and the parts that were hard to recognize.",
		],
		[
			"Exercise type: answering\nScore: 0.41\nCorrect: false\nQuestion: あなたは明日どうしますか?\nUser answer: I go yesterday store.\nReference answer: I went to the store yesterday.\nMetrics: {\"similarity\": 0.48, \"grammar_error_rate\": 0.57, \"token_difference_rate\": 0.50}",
			"The main idea is present, but the sentence structure needs correction. Review the verb tense and compare your word order with the reference answer.",
		],
	]

	def _build_prompt(self, context: dict[str, object]) -> list[dict[str, str]]:
		messages = [{"role": "system", "content": self.feedback_instruct}]

		for user_shot, assistant_shot in self.feedback_shots:
			messages.append({"role": "user", "content": user_shot})
			messages.append({"role": "assistant", "content": assistant_shot})

		messages.append({"role": "user", "content": json.dumps(context, ensure_ascii=False, indent=2)})
		return messages

	def _generate_with_model(self, context: dict[str, object]) -> str:
		if not self.model or not self.tokenizer:
			logger.warning("Text Generator Service is not available. Returning fallback feedback.")
			return self._fallback_feedback(context)

		try:
			messages = self._build_prompt(context)
			prompt = self.tokenizer.apply_chat_template(
				messages,
				tokenize=False,
				add_generation_prompt=True,
			)
			model_inputs = self.tokenizer([prompt], return_tensors="pt").to(self.model.device)

			generated_ids = self.model.generate(
				**model_inputs,
				max_new_tokens=96,
				do_sample=True,
				temperature=0.5,
				top_p=0.9,
			)
			generated_ids = [
				output_ids[len(input_ids):]
				for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
			]

			feedback = self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0].strip()
			return feedback or self._fallback_feedback(context)
		except Exception as err:
			logger.error(f"Failed to generate feedback with text model: {err}")
			return self._fallback_feedback(context)

	def _fallback_feedback(self, context: dict[str, object]) -> str:
		score = float(context.get("score", 0.0) or 0.0)
		correct = bool(context.get("correct", False))
		exercise_type = str(context.get("exercise_type", "exercise"))

		if correct:
			return (
				f"Good work on this {exercise_type} exercise. Your answer is correct, "
				"so the next step is to keep refining clarity and naturalness."
			)

		if score >= 0.75:
			return (
				f"You are close on this {exercise_type} exercise. Review the small differences between your answer "
				"and the reference, especially wording and sentence flow."
			)

		if score >= 0.5:
			return (
				f"You have the main idea for this {exercise_type} exercise, but part of the answer still needs work. "
				"Focus on the structure and compare your response with the reference."
			)

		return (
			f"This {exercise_type} exercise needs more review. Try the reference again and focus on the key words, "
			"grammar pattern, or pronunciation that changed the meaning."
		)

	def generate_feedback(
		self,
		ex_id: str,
		user_input: str,
		input_type: str,
		results: dict[str, object],
		threshold: float,
		correct_audio_index: int = 0,
		session: Optional[Session] = None,
		exercise=None,
	) -> str:
		owns_session = session is None and exercise is None
		if owns_session:
			session = db_manager.get_session()

		try:
			if exercise is None:
				exercise = exercise_service.get_by_id(ex_id, session=session)
			if not exercise:
				logger.warning(f"Exercise item not found when generating feedback: {ex_id}")
				return self._fallback_feedback({
					"score": results.get("score", 0.0),
					"correct": results.get("score", 0.0) > threshold,
					"exercise_type": input_type,
				})

			context: dict[str, object] = {
				"exercise_id": ex_id,
				"exercise_type": exercise.exercise_type,
				"question": exercise.question,
				"input_type": input_type,
				"score": round(float(results.get("score", 0.0) or 0.0), 3),
				"threshold": threshold,
				"correct": bool(results.get("score", 0.0) > threshold),
				"user_input": results.get("user_transcription", user_input) if input_type == "speech" else results.get("user_answer", user_input),
				"reference_answer": results.get("correct_transcription", exercise.answer) if input_type == "speech" else results.get("correct_answer", exercise.answer),
				"metrics": {
					key: value
					for key, value in results.items()
					if key not in {"score", "correct", "feedback"}
				},
			}

			if input_type == "speech":
				context["correct_audio_index"] = correct_audio_index

			return self._generate_with_model(context)
		except Exception as err:
			logger.error(f"Failed to generate feedback for Exercise {ex_id}: {err}")
			return self._fallback_feedback({
				"score": results.get("score", 0.0),
				"correct": results.get("score", 0.0) > threshold,
				"exercise_type": input_type,
			})
		finally:
			if owns_session:
				session.close()
