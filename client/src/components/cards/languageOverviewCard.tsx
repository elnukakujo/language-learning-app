"use client";

import { useRouter } from 'next/navigation';

type Language = {
    id: string;
    name: string;
    nativeName: string;
    flag: string;
    level: string;
    current_unit_id: string;
};

export default function LanguageOverviewCard({ language }: { language: Language }) {
    const router = useRouter();
    const handleCardClick = () => {
        router.push(`/languages/${language.id}`);
    };
    return (
        <button className="flex flex-col w-fit items-center p-4 border rounded-lg shadow-md" onClick={handleCardClick}>
            <h5>{language.name} ({language.nativeName}) {language.flag}</h5>
            <p>Level: {language.level}</p>
            <p>Current Unit ID: {language.current_unit_id}</p>
        </button>
    );
}