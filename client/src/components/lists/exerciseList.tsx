"use client";

import { useRouter, useParams } from "next/navigation";
import NavButton from "../buttons/navButton";

type ExerciseProps = {
    items: Array<{
        type: string;
        count: number;
    }>;
    count: number;
}

export default function ExerciseList({ exProps}: { exProps: ExerciseProps}) {
    const { language_id, unit_id } = useParams<{ language_id: string, unit_id: string }>();
    const router = useRouter()
    const handleClick = () => {
        router.push(`/languages/${language_id}/unit/${unit_id}/ex`)
    }
    return (
        <section className="flex flex-col gap-4 w-[14rem]">
            <h2>Exercises</h2>
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
        </section>
    );
}