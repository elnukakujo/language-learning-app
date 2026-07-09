"use client";

import { useParams, useRouter } from "next/navigation";
import NavButton from "@/components/layout/navButton";
import type Calligraphy from "@/interface/features/Calligraphy";

export default function CalligraphyList({ callProps}: { callProps: Calligraphy[]}) {
    const { language_id, lesson_id } = useParams<{ language_id: string, lesson_id: string }>();

    const router = useRouter();
    const handleClick = (id: string) => {
        router.push(`/languages/${language_id}/lesson/${lesson_id}/call/${id}`);
    };

    const averageScore = callProps.reduce((acc, item) => acc + item.score!, 0) / callProps.length;
    const averageDifficulty = callProps.reduce((acc, item) => acc + item.difficulty!, 0) / callProps.length;

    callProps.sort((a, b) => (a.score || 0) - (b.score || 0));

    return (
        <section className="card flex flex-col gap-4 w-[14rem]">
            <header>
                <h2>Calligraphy</h2>
                {callProps.length > 0 && (
                    <>
                        <p>Total: {callProps.length}</p>
                        <p>Average Score: {averageScore.toFixed(2)}/100</p>
                        <p>Average Difficulty: {averageDifficulty.toFixed(1)}</p>
                    </>
                )}
            </header>
            {callProps.length === 0 ? <p>Empty</p> :
                <ul className="list-item pl-5 space-y-1 list-none">
                    {callProps.map((item, index) => (
                        <li key={index}>
                            <button onClick={() => handleClick(item.id!)}>
                                {item.character.character} –{" "}{item.character.phonetic}
                            </button>
                        </li>
                    ))}
                </ul>
            }
            <NavButton
                path = {`/languages/${language_id}/lesson/${lesson_id}/call/new`}
            >
                <span>Add New Calligraphy</span>
            </NavButton>
            {callProps.length > 0 && (
            <NavButton
                path={`/languages/${language_id}/lesson/${lesson_id}/call/flashcard`}
            >
                <p>Flashcard Practice</p>
            </NavButton>)}
        </section>
    );
}