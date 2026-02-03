import { getElementbyId, getNext } from "@/api";
import NavButton from "@/components/buttons/navButton";
import DeleteButton from "@/components/buttons/deleteButton";
import Exercise from "@/interface/features/Exercise";

import FillInTheBlankExercise from "@/components/forms/exerciseForms/fillInTheBlankExercise";
import TranslateExercise from "@/components/forms/exerciseForms/translateExercise";
import EssayExercise from "@/components/forms/exerciseForms/essayExercise";
import TrueFalseExercise from "@/components/forms/exerciseForms/trueFalseExercise";
import OrganizeExercise from "@/components/forms/exerciseForms/organizeExercise";
import AnsweringExercise from "@/components/forms/exerciseForms/answeringExercise";
import MatchingExercise from "@/components/forms/exerciseForms/matchingExercise";
import BackButton from "@/components/buttons/backButton";

export default async function ExercisePage( { params } : { params: { language_id: string; unit_id: string; ex_id: string }}) {
    const { language_id, unit_id, ex_id } = await params;

    const exercise: Exercise = await getElementbyId(ex_id);

    return(
        <main className="flex flex-col space-y-4">
            {exercise.exercise_type === 'fill_in_the_blank' && (
                <FillInTheBlankExercise exercise={exercise} />
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