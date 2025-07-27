import { getElementbyId, getNext } from "@/api";
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
    const next_ex_id: string = await getNext(ex_id);

    const voc_associated = await Promise.all(exercise.associated_to?.vocabulary.map(id => getElementbyId(id)) || []);
    const char_associated = await Promise.all(exercise.associated_to?.characters.map(id => getElementbyId(id)) || []);
    const gram_associated = await Promise.all(exercise.associated_to?.grammar.map(id => getElementbyId(id)) || []);

    return(
        <main className="flex flex-col space-y-4">
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
            {exercise.associated_to && (
                <div>
                    {voc_associated && voc_associated.length > 0 && (
                        <div>
                            <p className="font-medium">Associated to the following vocabulary:</p>
                            <ul>
                                {voc_associated.map((item, index) => (
                                    <li key={index} className="w-fit px-2 py-1 border-2 border-gray-300 rounded-md cursor-pointer hover:opacity-80">{item.word} — {item.translation}</li>
                                ))}
                            </ul>
                        </div>
                    )}
                    {gram_associated && gram_associated.length > 0 && (
                        <div>
                            <p className="font-medium">Associated to the following grammar:</p>
                            <ul>
                                {gram_associated.map((item, index) => (
                                    <li key={index} className="w-fit px-2 py-1 border-2 border-gray-300 rounded-md cursor-pointer hover:opacity-80">{item.title}</li>
                                ))}
                            </ul>
                        </div>
                    )}
                    {char_associated && char_associated.length > 0 && (
                        <div>
                            <p className="font-medium">Associated to the following characters:</p>
                            <ul>
                                {char_associated.map((item, index) => (
                                    <li key={index} className="w-fit px-2 py-1 border-2 border-gray-300 rounded-md cursor-pointer hover:opacity-80">{item.character} - {item.meaning}</li>
                                ))}
                            </ul>
                        </div>
                    )}
                </div>
            )}
            <nav className="flex flex-row space-x-4">
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
            </nav>
        </main>
    )
}