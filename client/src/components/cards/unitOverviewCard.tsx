"use client";

import { useParams, useRouter } from 'next/navigation';
import Markdown from "react-markdown";

type Unit = {
    id: string;
    title: string;
    description: string;
    score: number;
    last_seen: Date;
};

export default function UnitOverviewCard({ unit }: { unit: Unit }) {
    const { language_id } = useParams();
    const router = useRouter();
    const handleClick = () => {
        router.push(`/languages/${language_id}/unit/${unit.id}`);
    };
    return (
        <button className="border rounded-lg p-4" onClick={handleClick}>
            <h3>{unit.title}</h3>
            <Markdown>{unit.description}</Markdown>
            <p>Score: {unit.score.toFixed(1)}/100</p>
        </button>
    );
}