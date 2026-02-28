"use client";

import { useParams, useRouter } from "next/navigation";
import NavButton from "../buttons/navButton";

import Vocabulary from "@/interface/features/Vocabulary";

export default function VocabularyList({ vocProps}: { vocProps: Vocabulary[]}) {
    const { language_id, unit_id } = useParams<{ language_id: string, unit_id: string }>();

    const router = useRouter();
    const handleClick = (id: string) => {
        router.push(`/languages/${language_id}/unit/${unit_id}/voc/${id}`);
    };

    const averageScore = vocProps.reduce((acc, item) => acc + item.score!, 0) / vocProps.length;

    vocProps.sort((a, b) => (a.score || 0) - (b.score || 0));

    return (
        <section className="flex flex-col gap-4 w-[14rem]">
            <header>
                <h2>Vocabulary</h2>
                {vocProps.length > 0 && (
                    <>
                        <p>Total: {vocProps.length}</p>
                        <p>Average Score: {averageScore.toFixed(2)}/100</p>
                    </>
                )}
            </header>
            {vocProps.length === 0 ? <p>Empty</p> :
                <ul className="list-item pl-5 space-y-1 list-none">
                    {vocProps.map((item, index) => (
                        <li key={index}>
                            <button onClick={() => handleClick(item.id!)}>
                                {item.word.word} –{" "}{item.word.translation}
                            </button>
                        </li>
                    ))}
                </ul>
            }
            <NavButton
                path = {`/languages/${language_id}/unit/${unit_id}/voc/new`}
            >
                <p>Add New Vocabulary</p>
            </NavButton>
            {vocProps.length > 0 && (
                <NavButton
                    path={`/languages/${language_id}/unit/${unit_id}/voc/flashcard`}
                >
                    <p>Flashcard Practice</p>
                </NavButton>
            )}
        </section>
    );
}