"use client";

import { useRouter } from 'next/navigation';

type Language = {
    language_id: string;
    name: string;
    native_name: string;
    flag: string;
    level: string;
    current_unit_id: string;
};

export default function LanguageOverviewCard({ language }: { language: Language }) {
    const router = useRouter();
    const handleCardClick = () => {
        router.push(`/languages/${language.language_id}`);
    };
    return (
        <button className="flex flex-col w-fit items-center p-4 border rounded-lg shadow-md" onClick={handleCardClick}>
            <h5>{language.name} ({language.native_name}) {language.flag}</h5>
            <p>Level: {language.level}</p>
            {language.current_unit_id && <p>Current Unit ID: {language.current_unit_id}</p>}
        </button>
    );
}