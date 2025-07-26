"use client";

import { useState, useEffect, useRef } from "react";
import NewElementButton from "@/components/buttons/newElementButton";
import ClassicSelectMenu from "@/components/selectMenu/classicSelectMenu";

export default function CreateExerciseForm({ unit_id }: { unit_id: string }) {
    const [exerciseType, setExerciseType] = useState<string>("")
    const [support, setSupport] = useState<string>("")
    const [question, setQuestion] = useState<string>("")
    const [answer, setAnswer] = useState<string>("")
    const [textareaToDisplay, setTextareaToDisplay] = useState<Array<string>>([]);

    const questionRef = useRef<HTMLTextAreaElement>(null);
    const supportRef = useRef<HTMLTextAreaElement>(null);
    const answerRef = useRef<HTMLTextAreaElement>(null);

    function useAutoResize(
          ref: React.RefObject<HTMLTextAreaElement | null>,
          value: string
        ) {
      useEffect(() => {
      const textarea = ref.current;
      if (textarea) {
        textarea.style.height = "auto";
        textarea.style.height = `${textarea.scrollHeight}px`;
      }
      }, [value, ref]);
    }

    useAutoResize(questionRef, question);
    useAutoResize(supportRef, support);
    useAutoResize(answerRef, answer);

    useEffect(() => {
      switch (exerciseType) {
        case "translate":
          setQuestion("Translate:");
          setSupport("-- A sentence to translate --");
          setAnswer("-- The translation --");
          setTextareaToDisplay(["question", "support", "answer"]);
          break;
        case "fill-in-the-blank":
          setQuestion("Fill the blanks in the following text:");
          setSupport("-- The house is __ and __. --");
          setAnswer("-- big__small --");
          setTextareaToDisplay(["question", "support", "answer"]);
          break;
        case "essay":
          setQuestion("Write an essay on a topic:");
          setSupport("-- Write here some requirements about the essay, and details --");
          setAnswer("-- Some helps and tips to write the essay --");
          setTextareaToDisplay(["question", "support", "answer"]);
          break;
        case "true-false":
          setQuestion("State whether the following statement is true or false:");
          setSupport("-- A statement to evaluate --");
          setAnswer("true");
          setTextareaToDisplay(["question", "support", "answer"]);
          break;
        case "organize":
          setQuestion("Organize the following items:");
          setSupport("-- My/house/small/purple/and/is --");
          setAnswer("-- My house is small and purple --");
          setTextareaToDisplay(["question", "support", "answer"]);
          break;
        case "answering":
          setQuestion("Answer the following question:");
          setSupport("-- A question to answer --");
          setAnswer("-- The answer to the question --");
          setTextareaToDisplay(["question", "support", "answer"]);
          break;
        default:
          setQuestion("");
          setSupport("");
          setAnswer("");
          setTextareaToDisplay([]);
          break;
      }
    }, [exerciseType]); 

    return (
      <form className="flex flex-col space-y-4 min-w-[40rem]">
        <ClassicSelectMenu
          options={[
            "translate",
            "fill-in-the-blank",
            "essay",
            "true-false",
            "organize",
            "answering",
          ]}
          selectedOption={exerciseType}
          onChange={setExerciseType}
        />
        {textareaToDisplay.includes("question") && (
          <section>
            <label htmlFor="question" className="block text-sm font-medium text-gray-700">
              Question
            </label>
            <textarea
              ref={questionRef}
              id="question"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              className="flex w-full overflow-hidden border border-gray-300 rounded-md p-2"
              required
            />
          </section>
        )}
        {textareaToDisplay.includes("support") && (
          <section>
            <label htmlFor="support" className="block text-sm font-medium text-gray-700">
              Support
            </label>
            <textarea
              ref={supportRef}
              id="support"
              value={support}
              onChange={(e) => setSupport(e.target.value)}
              className="flex w-full overflow-hidden border border-gray-300 rounded-md p-2"
              required
            />
          </section>
        )}
        {textareaToDisplay.includes("answer") && (
          <section>
            <label htmlFor="answer" className="block text-sm font-medium text-gray-700">
              Answer
            </label>
            {exerciseType === "true-false" ? (
              <div className="flex flex-row space-x-2">
                <span className="flex items-center space-x-2">
                  <input
                    id="answer-true"
                    type="radio"
                    checked={answer === "true"}
                    onChange={() => setAnswer("true")}
                    className="h-4 w-4 text-indigo-600 border-gray-300 rounded"
                    required
                  />
                  <label htmlFor="answer-true">True</label>
                </span>
                <span className="flex items-center space-x-2">
                  <input
                    id="answer-false"
                    type="radio"
                    checked={answer === "false"}
                    onChange={() => setAnswer("false")}
                    className="h-4 w-4 text-indigo-600 border-gray-300 rounded"
                    required
                  />
                  <label htmlFor="answer-false">False</label>
                </span>
              </div>)
              :
              <textarea
                ref={answerRef}
                id="answer"
                value={answer}
                onChange={(e) => setAnswer(e.target.value)}
                className="flex w-full overflow-hidden border border-gray-300 rounded-md p-2"
                required
              />
            }
          </section>
        )}
        {textareaToDisplay.length >= 1 && (
          <NewElementButton
            element={{
                type_element: "ex",
                id: "",
                exercise_type: exerciseType,
                question: question,
                support: support,
                answer: answer,
                score: 0.0,
                last_seen: new Date,
                unit_id: unit_id
          }}
        />
        )}
      </form>
    );
}