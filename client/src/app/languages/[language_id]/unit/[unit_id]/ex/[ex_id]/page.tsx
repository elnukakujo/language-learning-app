import { getElementbyId, getNextExercise } from "@/api";
import NavButton from "@/components/buttons/navButton";
import DeleteButton from "@/components/buttons/deleteButton";
import Exercise from "@/interface/Exercise";

import FillInTheBlankExercise from "@/components/forms/exerciseForms/fillInTheBlankExercise";
import TranslateExercise from "@/components/forms/exerciseForms/translateExercise";
import EssayExercise from "@/components/forms/exerciseForms/essayExercise";
import TrueFalseExercise from "@/components/forms/exerciseForms/trueFalseExercise";
import OrganizeExercise from "@/components/forms/exerciseForms/organizeExercise";
import AnsweringExercise from "@/components/forms/exerciseForms/answeringExercise";

export default async function ExercisePage( { params } : { params: { language_id: string; unit_id: string; ex_id: string }}) {
    const { language_id, unit_id, ex_id } = await params;

    const exercise: Exercise = await getElementbyId(ex_id);
    const next_ex_id: string = await getNextExercise(ex_id);
    console.log("Next Exercise ID:", next_ex_id);
    return(
        <main>
            {exercise.exercise_type === 'fill-in-the-blank' && (
                <FillInTheBlankExercise exercise={exercise} />
            )}
            {exercise.exercise_type === 'translate' && (
                <TranslateExercise exercise={ exercise } />
            )}
            {exercise.exercise_type === 'essay' && (
                <EssayExercise exercise={ exercise } />
            )}
            {exercise.exercise_type === 'true-false' && (
                <TrueFalseExercise exercise={ exercise } />
            )}
            {exercise.exercise_type === 'organize' && (
                <OrganizeExercise exercise={ exercise } />
            )}
            {exercise.exercise_type === 'answering' && (
                <AnsweringExercise exercise={ exercise } />
            )}
            <NavButton path={`/languages/${language_id}/unit/${unit_id}/ex/${exercise.id}/update`}>
                <p>Update the Exercise</p>
            </NavButton>
            <DeleteButton
                element_id={exercise.id}
            >
                <p>Delete Exercise</p>
            </DeleteButton>
            <NavButton path={`/languages/${language_id}/unit/${unit_id}/ex/${next_ex_id}`}>
                <p>Next Exercise</p>
            </NavButton>
        </main>
    )
}