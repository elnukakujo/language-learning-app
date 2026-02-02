"use client";

import { useRouter, useParams } from "next/navigation";
import NavButton from "../buttons/navButton";
import Exercise from "@/interface/features/Exercise";

export default function ExerciseList({ exProps}: { exProps: Exercise[]}) {
    const { language_id, unit_id } = useParams<{ language_id: string, unit_id: string }>();
    const router = useRouter()
    const handleClick = () => {
        router.push(`/languages/${language_id}/unit/${unit_id}/ex`)
    }

    const averageScore = exProps.reduce((acc, item) => acc + item.score!, 0) / exProps.length;

    const groupedExercises = exProps.reduce((groups: { [key: string]: Exercise[] }, exercise) => {
        const type = exercise.exercise_type || 'unknown';
        if (!groups[type]) {
            groups[type] = [];
        }
        groups[type].push(exercise);
        return groups;
    }, {});

    return (
        <section className="flex flex-col gap-4 w-[14rem]">
            <header>
                <h2>Exercises</h2>
                {exProps.length > 0 && (
                    <>
                        <p>Total: {exProps.length}</p>
                        <p>Average Score: {averageScore.toFixed(2)}/100</p>
                    </>
                )}
            </header>
            {exProps.length === 0 ? <p>Empty</p> :
                <ul className="list-item pl-5 space-y-1">
                    {Object.entries(groupedExercises).map(([type, exercises], index) => (
                        <li key={index}>
                            <button onClick={handleClick}>
                                Available {type.slice(0,1).toUpperCase()+type.slice(1)} : {" "} {exercises.length} 
                            </button>
                        </li>
                    ))}
                </ul>
            }
            <NavButton
                path = {`/languages/${language_id}/unit/${unit_id}/ex/new`}
            >
                <span>Add New Exercise</span>
            </NavButton>
            {exProps.length > 0 && (
                <NavButton 
                    path={`/languages/${language_id}/unit/${unit_id}/ex/${
                            unit_id+"_E"+Number(Math.floor(Math.random() * exProps.length)+1)
                        }`}
                >
                    <p>Exercise Practice</p>
                </NavButton>)}
        </section>
    );
}