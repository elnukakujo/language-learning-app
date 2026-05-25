"use client";

import { useRouter } from 'next/navigation';
import type Language from '@/interface/containers/Language';

export default function LanguageOverviewCard({ language }: { language: Language }) {
    const router = useRouter();

    const handleCardClick = () => {
        router.push(`/languages/${language.id}`);
    };
    return (
        <button className="flex flex-col w-fit items-center p-4 border rounded-lg shadow-md" onClick={handleCardClick}>
            <p>{language.flag}</p>
            <h3>{language.name} ({language.alias})</h3>
            <h5>{language.level}</h5>
            <p>{language.score!.toFixed(1)}/100</p>
            <p>Status: {language.status}</p>
            <p>Created at: {new Date(language.created_at || 0).toLocaleDateString('en-US')}</p>
            <p>Last Seen: {new Date(language.last_seen_at).toLocaleDateString('en-US')}</p>
            {language.current_lesson_id && <p>{language.current_lesson_id}</p>}
        </button>
    );
}