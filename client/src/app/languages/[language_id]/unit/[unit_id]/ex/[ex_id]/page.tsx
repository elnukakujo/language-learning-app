import { getElementbyId } from "@/api";
import NavButton from "@/components/buttons/navButton";
import DeleteButton from "@/components/buttons/deleteButton";
import Exercise from "@/interface/Exercise";

import FillInTheBlankExercise from "@/components/forms/exerciseForms/FillInTheBlankExercise";
import TranslateExercise from "@/components/forms/exerciseForms/translateExercise";
import EssayExercise from "@/components/forms/exerciseForms/essayExercise";

export default async function ExercisePage( { params } : { params: { language_id: string; unit_id: string; ex_id: string }}) {
    const { language_id, unit_id, ex_id } = await params;

    const exercise: Exercise = await getElementbyId(ex_id);

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
            <NavButton path={`/languages/${language_id}/unit/${unit_id}/ex/${exercise.id}/update`}>
                <p>Update the Exercise</p>
            </NavButton>
            <DeleteButton
                element_id={exercise.id}
            >
                <p>Delete Exercise</p>
            </DeleteButton>
        </main>
    )
}