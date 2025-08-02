"use client";

import { useParams, useRouter } from "next/navigation";
import NavButton from "../buttons/navButton";

type CharactersProps = {
    items: Array<{
        id: string;
        character: string;
        meaning: string;
        score: number;
    }>;
    count: number;
};

export default function CharacterList({ charProps}: { charProps: CharactersProps}) {
    const { language_id, unit_id } = useParams<{ language_id: string, unit_id: string }>();

    const router = useRouter();
    const handleClick = (id: string) => {
        router.push(`/languages/${language_id}/unit/${unit_id}/char/${id}`);
    };

    const averageScore = charProps.items.reduce((acc, item) => acc + item.score, 0) / charProps.count;

    return (
        <section className="flex flex-col gap-4 w-[14rem]">
            <header>
                <h2>Characters</h2>
                {charProps.count > 0 && (
                    <>
                        <p>Total: {charProps.count}</p>
                        <p>Average Score: {averageScore.toFixed(2)}/100</p>
                    </>
                )}
            </header>
            {charProps.count === 0 ? <p>Empty</p> :
                <ul className="list-item pl-5 space-y-1">
                    {charProps.items.map((item, index) => (
                        <li key={index}>
                            <button onClick={() => handleClick(item.id)}>
                                {(item as CharactersProps["items"][0]).character} –{" "}{(item as CharactersProps["items"][0]).meaning}
                            </button>
                        </li>
                    ))}
                </ul>
            }
            <NavButton
                path = {`/languages/${language_id}/unit/${unit_id}/char/new`}
            >
                <span>Add New Character</span>
            </NavButton>
            {charProps.items.length > 0 && (
            <NavButton
                path={`/languages/${language_id}/unit/${unit_id}/char/${
                        charProps.items[Math.floor(Math.random() * charProps.items.length)].id
                    }/flashcard`}
            >
                <p>Flashcard Practice</p>
            </NavButton>)}
        </section>
    );
}