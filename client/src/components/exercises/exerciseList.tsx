"use client";

import { useParams } from "next/navigation";
import NavButton from "@/components/layout/navButton";
import Exercise from "@/interface/features/Exercise";

export default function ExerciseList({ exProps}: { exProps: Exercise[]}) {
    const { language_id, lesson_id } = useParams<{ language_id: string, lesson_id: string }>();

    const averageScore = exProps.reduce((acc, item) => acc + item.score!, 0) / exProps.length;
    const averageDifficulty = exProps.reduce((acc, item) => acc + item.difficulty!, 0) / exProps.length;

    return (
        <section className="card flex flex-col gap-4 w-[14rem]">
            <header>
                <h2>Exercises</h2>
                {exProps.length > 0 ? (
                    <>
                        <p>Total: {exProps.length}</p>
                        <p>Average Score: {averageScore.toFixed(2)}/100</p>
                        <p>Average Difficulty: {averageDifficulty.toFixed(1)}</p>
                    </>
                ) : (
                    <p>Empty</p>
                )}
            </header>
            <NavButton path={`/languages/${language_id}/lesson/${lesson_id}/ex`}>
                <span>See Exercises</span>
            </NavButton>
            <NavButton
                path = {`/languages/${language_id}/lesson/${lesson_id}/ex/new`}
            >
                <span>Add New Exercise</span>
            </NavButton>
            {exProps.length > 0 && (
                <NavButton
                    path={`/languages/${language_id}/lesson/${lesson_id}/ex/practice`}
                >
                    <p>Exercise Practice</p>
                </NavButton>)}
        </section>
    );
}
