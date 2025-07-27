import { getExercisesOverview } from "@/api";
import NavButton from "@/components/buttons/navButton";
import DeleteButton from "@/components/buttons/deleteButton";
import Exercise from "@/interface/Exercise";
import Markdown from "react-markdown";

export default async function ExercisesPage({ params }: { params: { language_id: string, unit_id: string } }){
    const { language_id, unit_id } = await params;

    const exercises: Exercise[] = await getExercisesOverview(unit_id)
    const exercisesByType = exercises.reduce((group, exercise) => {
        const key = exercise.exercise_type || "unknown";
        if (!group[key]) {
            group[key] = [];
        }
        group[key].push(exercise);
        return group;
    }, {} as Record<string, Exercise[]>);

    return(
        <main className="flex flex-col space-y-5">
            <h1>Exercises</h1>
            <article className="flex flex-col space-y-5">
                {Object.entries(exercisesByType).map(([type, exercises]) => (
                    <section key={type}>
                        <h3>{type.charAt(0).toUpperCase() + type.slice(1)}</h3>
                        <ul>
                            {exercises.map((exercise, index) => (
                                <li key={index}>
                                    <Markdown>{exercise.question}</Markdown>
                                    <p>Score: {exercise.score?.toFixed(2)}/100</p>
                                    <nav className="flex flex-row space-x-2">
                                        <NavButton path={`/languages/${language_id}/unit/${unit_id}/ex/${exercise.id}`}>
                                            <p>Practice this Exercise</p>
                                        </NavButton>
                                        <NavButton path={`/languages/${language_id}/unit/${unit_id}/ex/${exercise.id}/update`}>
                                            <p>Update the Exercise</p>
                                        </NavButton>
                                        <DeleteButton element_id={exercise.id}>
                                            <p>Delete Exercise</p>
                                        </DeleteButton>
                                    </nav>
                                </li>
                            ))}
                        </ul>
                    </section>
                ))}
            </article>
            <NavButton path={`/languages/${language_id}/unit/${unit_id}/ex/new`}>
                <p>Add New Exercise</p>
            </NavButton>
        </main>
    )
}