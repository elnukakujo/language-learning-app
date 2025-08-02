"use client";

import { useParams, useRouter } from "next/navigation";
import NavButton from "../buttons/navButton";

type GrammarProps = {
    items: Array<{
        id: string;
        title: string;
        score: number;
    }>;
    count: number;
};

export default function GrammarList({ gramProps}: { gramProps: GrammarProps}) {
    const { language_id, unit_id } = useParams<{ language_id: string, unit_id: string }>();

    const router = useRouter();
    const handleClick = (id: string) => {
        router.push(`/languages/${language_id}/unit/${unit_id}/gram/${id}`);
    };

    const averageScore = gramProps.items.reduce((acc, item) => acc + item.score, 0) / gramProps.count;

    return (
        <section className="flex flex-col gap-4 w-[14rem]">
            <header>
                <h2>Grammar</h2>
                {gramProps.count > 0 && (
                    <>
                        <p>Total: {gramProps.count}</p>
                        <p>Average Score: {averageScore.toFixed(2)}/100</p>
                    </>
                )}
            </header>
            {gramProps.count === 0 ? <p>Empty</p> :
                <ul className="list-item pl-5 space-y-1">
                    {gramProps.items.map((item, index) => (
                        <li key={index}>
                            <button onClick={() => handleClick(item.id)}>
                                {(item as GrammarProps["items"][0]).title}
                            </button>
                        </li>
                    ))}
                </ul>
            }
            <NavButton
                path = {`/languages/${language_id}/unit/${unit_id}/gram/new`}
            >
                <span>Add New Grammar</span>
            </NavButton>
        </section>
    );
}