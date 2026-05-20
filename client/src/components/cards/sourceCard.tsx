"use client";

import { useEffect, useState } from 'react';
import Calligraphy from '@/interface/features/Calligraphy';
import Exercise from '@/interface/features/Exercise';
import Grammar from '@/interface/features/Grammar';
import Vocabulary from '@/interface/features/Vocabulary';
import Source from '@/interface/systemData/Source';
import Lesson from '@/interface/containers/Lesson';
import Language from '@/interface/containers/Language';
import { getVocabularyById } from '@/api/vocabulary';
import { getCalligraphyById } from '@/api/calligraphy';
import { getGrammarById } from '@/api/grammar';
import { getExerciseById } from '@/api/exercise';
import { getLessonById } from '@/api/lesson';
import { getLanguageById } from '@/api/language';

interface RelatedElementsProps {
    voc?: Vocabulary[];
    call?: Calligraphy[];
    gram?: Grammar[];
    ex?: Exercise[];
    lesson?: Lesson[];
    lang?: Language[];
}

export default function SourceCard({source}: { source: Source }) {
    const [relatedElements, setRelatedElements] = useState<RelatedElementsProps>({});

    console.log("Rendering SourceCard for source", source.id, "with initial elements", source.elements);

    useEffect(() => {
        let isMounted = true;

        const loadRelatedElements = async (): Promise<void> => {
            if (!source.elements) {
                if (isMounted) setRelatedElements({});
                return;
            }

            const elements = source.elements as Record<string, string[] | undefined>;

            const [voc, call, gram, ex, lesson, lang] = await Promise.all([
                elements["voc"] ? Promise.all(elements["voc"].map((id: string) => getVocabularyById(id))) : [],
                elements["call"] ? Promise.all(elements["call"].map((id: string) => getCalligraphyById(id))) : [],
                elements["gram"] ? Promise.all(elements["gram"].map((id: string) => getGrammarById(id))) : [],
                elements["ex"] ? Promise.all(elements["ex"].map((id: string) => getExerciseById(id))) : [],
                elements["lesson"] ? Promise.all(elements["lesson"].map((id: string) => getLessonById(id))) : [],
                elements["lang"] ? Promise.all(elements["lang"].map((id: string) => getLanguageById(id))) : []
            ]);

            if (isMounted) {
                setRelatedElements({ voc, call, gram, ex, lesson, lang });
            }
        };

        loadRelatedElements();
        
        console.log("Related elements for source", source.id, relatedElements);

        return () => {
            isMounted = false;
        };
    }, [source]);

    return (
        <div className="pl-4 py-3 border-l-2 border-white/20">
            <div className="flex items-baseline gap-3 mb-1">
                <h2 className="text-base font-medium">{source.title}</h2>
                <span className="text-xs opacity-40">{source.date}</span>
                <span className="text-xs opacity-40">{source.source_type}</span>
            </div>
            <p className="text-sm opacity-60 mb-3">{source.description}</p>

            {relatedElements && (
                <div className="flex flex-col gap-1.5">
                {[
                    { key: "voc",    label: "Vocab",    text: relatedElements.voc?.map((i: Vocabulary)  => i.word?.word           ?? "").filter(Boolean).join(" · ") },
                    { key: "call",   label: "Calli",    text: relatedElements.call?.map((i: Calligraphy) => i.character?.character ?? "").filter(Boolean).join(" · ") },
                    { key: "gram",   label: "Grammar",  text: relatedElements.gram?.map((i: Grammar)     => i.title               ?? "").filter(Boolean).join(" · ") },
                    { key: "ex",     label: "Exercise", text: relatedElements.ex?.map((i: Exercise)      => i.question            ?? "").filter(Boolean).join(" · ") },
                    { key: "lesson", label: "Lesson",   text: relatedElements.lesson?.map((i: Lesson)    => i.title               ?? "").filter(Boolean).join(" · ") },
                    { key: "lang",   label: "Lang",     text: relatedElements.lang?.map((i: Language)    => i.name                ?? "").filter(Boolean).join(" · ") },
                ]
                    .filter((s) => Boolean(s.text))
                    .map(({ key, label, text }) => (
                    <div key={key} className="flex gap-2 text-xs items-baseline">
                        <span className="opacity-40 w-14 shrink-0">{label}</span>
                        <span className="opacity-85">{text}</span>
                    </div>
                    ))}
                </div>
            )}
        </div>
    );
}