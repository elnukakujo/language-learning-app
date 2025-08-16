"use client";

import { useRouter, useParams } from "next/navigation";
import NavButton from "../buttons/navButton";

type ExerciseProps = {
    items: Array<{
        type: string;
        count: number;
        score: number;
    }>;
    count: number;
}

export default function ExerciseList({ exProps}: { exProps: ExerciseProps}) {
    const { language_id, unit_id } = useParams<{ language_id: string, unit_id: string }>();
    const router = useRouter()
    const handleClick = () => {
        router.push(`/languages/${language_id}/unit/${unit_id}/ex`)
    }

    const averageScore = exProps.items.reduce((acc, item) => acc + item.score, 0) / exProps.items.length;

    console.log(exProps.count);

    return (
        <section className="flex flex-col gap-4 w-[14rem]">
            <header>
                <h2>Exercises</h2>
                {exProps.count > 0 && (
                    <>
                        <p>Total: {exProps.count}</p>
                        <p>Average Score: {averageScore.toFixed(2)}/100</p>
                    </>
                )}
            </header>
            {exProps.count === 0 ? <p>Empty</p> :
                <ul className="list-item pl-5 space-y-1">
                    {exProps.items.map((item, index) => (
                        <li key={index}>
                            <button onClick={handleClick}>
                                Available {item.type.slice(0,1).toUpperCase()+item.type.slice(1)} : {" "} {item.count} 
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
            {exProps.items.length > 0 && (
                <NavButton 
                    path={`/languages/${language_id}/unit/${unit_id}/ex/${
                            unit_id+"_E"+Number(Math.floor(Math.random() * exProps.count)+1)
                        }`}
                >
                    <p>Exercise Practice</p>
                </NavButton>)}
        </section>
    );
}