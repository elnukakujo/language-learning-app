import { getElementbyId } from "@/api";
import NavButton from "@/components/buttons/navButton";
import DeleteButton from "@/components/buttons/deleteButton";
import Exercise from "@/interface/features/Exercise";

import TypeInTheBlankExercise from "@/components/forms/exerciseForms/typeInTheBlankExercise";
import SelectInTheBlankExercise from "@/components/forms/exerciseForms/selectInTheBlankExercise";
import TranslateExercise from "@/components/forms/exerciseForms/translateExercise";
import EssayExercise from "@/components/forms/exerciseForms/essayExercise";
import TrueFalseExercise from "@/components/forms/exerciseForms/trueFalseExercise";
import OrganizeExercise from "@/components/forms/exerciseForms/organizeExercise";
import AnsweringExercise from "@/components/forms/exerciseForms/answeringExercise";
import MatchingExercise from "@/components/forms/exerciseForms/matchingExercise";
import SpeakingExercise from "@/components/forms/exerciseForms/speakingExercise";
import BackButton from "@/components/buttons/backButton";
import ConversationExercise from "@/components/forms/exerciseForms/conversationExercise";

export default async function ExercisePage( { params } : { params: { language_id: string; unit_id: string; ex_id: string }}) {
    const { language_id, unit_id, ex_id } = await params;

    const exercise: Exercise = await getElementbyId(ex_id);

    return(
        <main className="flex flex-col space-y-4">
            {exercise.exercise_type === 'type_in_the_blank' && (
                <TypeInTheBlankExercise exercise={exercise} />
            )}
            {exercise.exercise_type === 'select_in_the_blank' && (
                <SelectInTheBlankExercise exercise={exercise} />
            )}
            {exercise.exercise_type === 'translate' && (
                <TranslateExercise exercise={ exercise } />
            )}
            {exercise.exercise_type === 'essay' && (
                <EssayExercise exercise={ exercise } />
            )}
            {exercise.exercise_type === 'true_false' && (
                <TrueFalseExercise exercise={ exercise } />
            )}
            {exercise.exercise_type === 'organize' && (
                <OrganizeExercise exercise={ exercise } />
            )}
            {exercise.exercise_type === 'answering' && (
                <AnsweringExercise exercise={ exercise } />
            )}
            {exercise.exercise_type === 'matching' && (
                <MatchingExercise exercise={ exercise } />
            )}
            {exercise.exercise_type === 'speaking' && (
                <SpeakingExercise exercise={ exercise } />
            )}
            {exercise.exercise_type === 'conversation' && <ConversationExercise exercise={exercise} />}

            <nav className="flex flex-row space-x-4">
                <NavButton path={`/languages/${language_id}/unit/${unit_id}/ex/${exercise.id}/update`}>
                    <p>Update the Exercise</p>
                </NavButton>
                <DeleteButton
                    element_id={exercise.id!}
                >
                    <p>Delete Exercise</p>
                </DeleteButton>
                <BackButton>
                    <p>Back to Unit</p>
                </BackButton>
            </nav>
        </main>
    )
}