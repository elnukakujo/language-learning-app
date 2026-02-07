"use client";

import { useParams, useRouter } from "next/navigation";
import NavButton from "../buttons/navButton";
import type Calligraphy from "@/interface/features/Calligraphy";

export default function CalligraphyList({ callProps}: { callProps: Calligraphy[]}) {
    const { language_id, unit_id } = useParams<{ language_id: string, unit_id: string }>();

    const router = useRouter();
    const handleClick = (id: string) => {
        router.push(`/languages/${language_id}/unit/${unit_id}/call/${id}`);
    };

    const averageScore = callProps.reduce((acc, item) => acc + item.score!, 0) / callProps.length;

    return (
        <section className="flex flex-col gap-4 w-[14rem]">
            <header>
                <h2>Calligraphy</h2>
                {callProps.length > 0 && (
                    <>
                        <p>Total: {callProps.length}</p>
                        <p>Average Score: {averageScore.toFixed(2)}/100</p>
                    </>
                )}
            </header>
            {callProps.length === 0 ? <p>Empty</p> :
                <ul className="list-item pl-5 space-y-1">
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
                path = {`/languages/${language_id}/unit/${unit_id}/call/new`}
            >
                <span>Add New Calligraphy</span>
            </NavButton>
            {callProps.length > 0 && (
            <NavButton
                path={`/languages/${language_id}/unit/${unit_id}/call/flashcard`}
            >
                <p>Flashcard Practice</p>
            </NavButton>)}
        </section>
    );
}