"use client";

import { useParams, useRouter } from "next/navigation";
import NavButton from "@/components/layout/navButton";

import Vocabulary from "@/interface/features/Vocabulary";

export default function VocabularyList({ vocProps}: { vocProps: Vocabulary[]}) {
    const { language_id, lesson_id } = useParams<{ language_id: string, lesson_id: string }>();

    const router = useRouter();
    const handleClick = (id: string) => {
        router.push(`/languages/${language_id}/lesson/${lesson_id}/voc/${id}`);
    };

    const averageScore = vocProps.reduce((acc, item) => acc + item.score!, 0) / vocProps.length;
    const averageDifficulty = vocProps.reduce((acc, item) => acc + item.difficulty!, 0) / vocProps.length;

    vocProps.sort((a, b) => (a.score || 0) - (b.score || 0));

    return (
        <section className="card flex flex-col gap-4 w-[14rem]">
            <header>
                <h2>Vocabulary</h2>
                {vocProps.length > 0 && (
                    <>
                        <p>Total: {vocProps.length}</p>
                        <p>Average Score: {averageScore.toFixed(2)}/100</p>
                        <p>Average Difficulty: {averageDifficulty.toFixed(1)}</p>
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
                path = {`/languages/${language_id}/lesson/${lesson_id}/voc/new`}
            >
                <p>Add New Vocabulary</p>
            </NavButton>
            {vocProps.length > 0 && (
                <NavButton
                    path={`/languages/${language_id}/lesson/${lesson_id}/voc/flashcard`}
                >
                    <p>Flashcard Practice</p>
                </NavButton>
            )}
        </section>
    );
}