"use client";

import { useParams, useRouter } from "next/navigation";
import NavButton from "../buttons/navButton";
import Grammar from "@/interface/features/Grammar";

export default function GrammarList({ gramProps}: { gramProps: Grammar[]}) {
    const { language_id, unit_id } = useParams<{ language_id: string, unit_id: string }>();

    const router = useRouter();
    const handleClick = (id: string) => {
        router.push(`/languages/${language_id}/unit/${unit_id}/gram/${id}`);
    };

    const averageScore = gramProps.reduce((acc, item) => acc + item.score!, 0) / gramProps.length;
    gramProps.sort((a, b) => (a.score || 0) - (b.score || 0));

    return (
        <section className="flex flex-col gap-4 w-[14rem]">
            <header>
                <h2>Grammar</h2>
                {gramProps.length > 0 && (
                    <>
                        <p>Total: {gramProps.length}</p>
                        <p>Average Score: {averageScore.toFixed(2)}/100</p>
                    </>
                )}
            </header>
            {gramProps.length === 0 ? <p>Empty</p> :
                <ul className="list-item pl-5 space-y-1 list-none">
                    {gramProps.map((item, index) => (
                        <li key={index}>
                            <button onClick={() => handleClick(item.id!)}>
                                {item.title}
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

            {gramProps.length > 0 && (
                <NavButton
                    path={`/languages/${language_id}/unit/${unit_id}/gram/flashcard`}
                >
                    <p>Flashcard Practice</p>
                </NavButton>)
            }
        </section>
    );
}