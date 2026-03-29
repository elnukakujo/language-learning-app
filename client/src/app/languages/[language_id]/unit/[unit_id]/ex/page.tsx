import { getExercisesByUnit } from "@/api";
import NavButton from "@/components/buttons/navButton";
import DeleteButton from "@/components/buttons/deleteButton";
import Exercise from "@/interface/features/Exercise";
import Markdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { cleanString } from "@/utils/clean_string";

export default async function ExercisesPage({ params }: { params: { language_id: string, unit_id: string } }){
    const { language_id, unit_id } = await params;

    const exercises: Exercise[] = await getExercisesByUnit(unit_id)
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
            <article className="flex flex-col space-y-4">
                {Object.entries(exercisesByType).map(([type, exercises]) => (
                    <section key={type}>
                        <h3>{type.charAt(0).toUpperCase() + type.slice(1)}</h3>
                        <ul>
                            {exercises.map((exercise, index) => (
                                <li key={index} className="flex flex-col gap-2">
                                    {!['fill_in_the_blank', 'conversation'].includes(exercise.exercise_type!) && (
                                        <Markdown remarkPlugins={[remarkGfm]}>{exercise.question}</Markdown>
                                    )}
                                    {exercise.exercise_type === 'fill_in_the_blank' && (
                                        <span className="flex flex-row gap-2">
                                            {
                                                exercise.question.split('\n\n').map((part, idx) => (
                                                    <p
                                                        key={idx}
                                                    >
                                                        {part === '__' ? <span className="underline">[Blank]</span> : part}
                                                    </p>
                                                ))
                                            }
                                        </span>
                                    )}
                                    {exercise.exercise_type === 'conversation' && (() => {
                                        const lines: {speakerId: string}[] = JSON.parse(exercise.question).lines;
                                        const speakers: {id: string, name: string, isUser: boolean}[] = JSON.parse(exercise.question).speakers;

                                        const userId = speakers.filter((speaker) => speaker.isUser)[0]?.id;
                                        const userLines = lines.filter((line) => line.speakerId === userId);
                                        return (
                                            <span className="flex flex-col">
                                                <p>Total Exchanges: {lines.length}</p>
                                                <p>User Lines: {userLines.length}</p>
                                                <p>Unique Speakers: {speakers.length}</p>
                                            </span>
                                        );
                                    })()}
                                    <p>Score: {exercise.score?.toFixed(2)}/100</p>
                                    <nav className="flex flex-row space-x-2">
                                        <NavButton path={`/languages/${language_id}/unit/${unit_id}/ex/${exercise.id}`}>
                                            <p>Practice this Exercise</p>
                                        </NavButton>
                                        <NavButton path={`/languages/${language_id}/unit/${unit_id}/ex/${exercise.id}/update`}>
                                            <p>Update the Exercise</p>
                                        </NavButton>
                                        <DeleteButton element_id={exercise.id!}>
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