import { getExercisesOverview } from "@/api";
import NavButton from "@/components/buttons/navButton";
import DeleteButton from "@/components/buttons/deleteButton";
import Exercise from "@/interface/Exercise";
import Markdown from "react-markdown";

export default async function ExercisesPage({ params }: { params: { language_id: string, unit_id: string } }){
    const { language_id, unit_id } = await params;

    const exercises: Exercise[] = await getExercisesOverview(unit_id)

    return(
        <main className="flex flex-col space-y-5">
            <h1>Exercises</h1>
            {exercises.map((exercise,index) => (
                <section key={index}>
                    {exercise.exercise_type && <h6><i>{exercise.exercise_type?.charAt(0).toUpperCase() + exercise.exercise_type?.slice(1)}</i></h6>}
                    <Markdown>{exercise.question}</Markdown>
                    <nav className="flex flex-row space-x-2">
                        <NavButton path={`/languages/${language_id}/unit/${unit_id}/ex/${exercise.id}`}>
                            <p>See the Exercise</p>
                        </NavButton>
                        <NavButton path={`/languages/${language_id}/unit/${unit_id}/ex/${exercise.id}/update`}>
                            <p>Update the Informations</p>
                        </NavButton>
                        <DeleteButton element_id={exercise.id}/>
                    </nav>
                </section>
            ))}
            <NavButton path={`/languages/${language_id}/unit/${unit_id}/ex/new`}>
                <p>Add New Exercise</p>
            </NavButton>
        </main>
    )
}