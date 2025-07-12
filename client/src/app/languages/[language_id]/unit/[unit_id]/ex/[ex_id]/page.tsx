import { getElementbyId } from "@/api";
import NavButton from "@/components/buttons/navButton";
import Exercise from "@/interface/Exercise";
import Markdown from "react-markdown";

export default async function ExercisePage( { params } : { params: { language_id: string; unit_id: string; ex_id: string }}) {
    const { language_id, unit_id, ex_id } = await params;

    const exercise: Exercise = await getElementbyId(ex_id);

    return(
        <main>
            {exercise.exercise_type && <h6><i>{exercise.exercise_type?.charAt(0).toUpperCase() + exercise.exercise_type?.slice(1)}</i></h6>}
            <Markdown>{exercise.question}</Markdown>
            <NavButton path={`/languages/${language_id}/unit/${unit_id}/ex/${exercise.id}/update`}>
                <p>Update the Informations</p>
            </NavButton>
        </main>
    )
}