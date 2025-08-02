"use client";

import { getNext } from "@/api";
import { useParams, useRouter } from "next/navigation";
import NavButton from "../buttons/navButton";

type VocabularyProps = {
    items: Array<{
        id: string;
        word: string;
        translation: string;
        score: number;
    }>;
    count: number;
};

export default function VocabularyList({ vocProps}: { vocProps: VocabularyProps}) {
    const { language_id, unit_id } = useParams<{ language_id: string, unit_id: string }>();

    const router = useRouter();
    const handleClick = (id: string) => {
        router.push(`/languages/${language_id}/unit/${unit_id}/voc/${id}`);
    };

    const averageScore = vocProps.items.reduce((acc, item) => acc + item.score, 0) / vocProps.count;

    return (
        <section className="flex flex-col space-y-2 w-[14rem]">
            <header>
                <h2>Vocabulary</h2>
                {vocProps.count > 0 && (
                    <>
                        <p>Total: {vocProps.count}</p>
                        <p>Average Score: {averageScore.toFixed(2)}/100</p>
                    </>
                )}
            </header>
            {vocProps.count === 0 ? <p>Empty</p> :
                <ul className="list-item pl-5 space-y-1">
                    {vocProps.items.map((item, index) => (
                        <li key={index}>
                            <button onClick={() => handleClick(item.id)}>
                                {(item as VocabularyProps["items"][0]).word} –{" "}{(item as VocabularyProps["items"][0]).translation}
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
            <NavButton
                path={`/languages/${language_id}/unit/${unit_id}/voc/${
                    vocProps.items[Math.floor(Math.random() * vocProps.items.length)].id
                }/flashcard`}
            >
                <p>Flashcard Practice</p>
            </NavButton>
        </section>
    );
}