"use client";

import { useRouter } from 'next/navigation';
import type Language from '@/interface/containers/Language';
import { languageProficiencySystems } from '@/utils/language_iso639';
import ScoreDisplay from '../ui/displays/scoreDisplay';

export default function LanguageOverviewCard({ language }: { language: Language }) {
    const router = useRouter();

    const handleCardClick = () => {
        router.push(`/languages/${language.id}`);
    };

    const system = languageProficiencySystems[language.target_iso639_2t ?? ""];
    const levelLabel = system?.levels[language.level]?.code ?? `Level ${language.level}`;

    return (
        <button
            className="card flex h-48 w-48 shrink-0 flex-col items-center justify-center gap-1 overflow-hidden text-center cursor-pointer transition hover:-translate-y-0.5 hover:bg-accent-soft hover:shadow-md"
            onClick={handleCardClick}
        >
            <header>
                <p className="text-2xl">{language.flag}</p>
                <h3 className="font-serif text-lg text-ink line-clamp-1">{language.name} ({language.alias})</h3>
                <h5 className="text-xs uppercase tracking-wide text-muted">{levelLabel}</h5>
            </header>
            <div className="index-divider w-full">
                <ScoreDisplay score={language.score} />
                <p className="text-sm text-muted">Status: {language.status}</p>
            </div>
        </button>
    );
}