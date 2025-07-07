"use client";

import { useRouter } from 'next/navigation';

type Language = {
    id: string;
    name: string;
    native_name: string;
    flag: string;
    level: string;
    current_unit_id: string;
    description?: string;
    score: number;
    last_seen: Date;
};

export default function LanguageOverviewCard({ language }: { language: Language }) {
    const router = useRouter();
    const handleCardClick = () => {
        router.push(`/languages/${language.id}`);
    };
    return (
        <button className="flex flex-col w-fit items-center p-4 border rounded-lg shadow-md" onClick={handleCardClick}>
            <h5>{language.flag}</h5>
            <h5>{language.name} ({language.native_name})</h5>
            <p>{language.level}</p>
            <p>{language.score.toFixed(1)}/100</p>
            <p>Last Seen: {new Date(language.last_seen).toLocaleDateString()}</p>
            {language.current_unit_id && <p>{language.current_unit_id}</p>}
        </button>
    );
}