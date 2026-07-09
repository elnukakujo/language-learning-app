"use client";

import type Grammar from "@/interface/features/Grammar";
import { useEffect, useRef, useState } from "react";
import { updateScoreById } from "@/api/process";
import BackButton from "@/components/ui/buttons/backButton";
import GrammarCard from "./grammarCard";
import ElementTagsCard from "./elementTagsCard";
import SentenceCard from "./sentenceCard";
import ElementPerformanceCard from "./elementPerformanceCard";
import ElementSourcesCard from "./elementSourcesCard";
import WordCard from "./wordCard";

export default function GrammarFlashCard({ grammars }: { grammars: Grammar[] }) {
    const [currentIndex, setCurrentIndex] = useState<number>(0);
    const grammar: Grammar = grammars[currentIndex];
    const startTimeRef = useRef<number>(performance.now());
    const [hintUsed, setHintUsed] = useState<boolean>(false);
    const [hiddenTranslation, setHiddenTranslation] = useState<boolean>(true);

    useEffect(() => {
        startTimeRef.current = performance.now();
        setHintUsed(false);
        setHiddenTranslation(true);
    }, [currentIndex]);

    const reveal = () => {
        if (!hiddenTranslation) return;
        setHiddenTranslation(false);
        setHintUsed(true);
    };

    const handleGoNext = () => {
        const duration_ms = Math.round(performance.now() - startTimeRef.current);
        updateScoreById(grammar.id!, 1, duration_ms, hintUsed);
        setCurrentIndex(currentIndex + 1);
    }

    return (
        <article>
            <h3>{currentIndex + 1} / {grammars.length}</h3>
            <section className="flex flex-col space-y-4">
                <h1>Grammar Sheet</h1>
                <div className="flashcard">
                    <div className={`flashcard-inner ${!hiddenTranslation ? "is-flipped" : ""}`}>
                        <div
                            className="flashcard-face card cursor-pointer flex flex-col space-y-4"
                            role="button"
                            tabIndex={0}
                            onClick={reveal}
                            onKeyDown={(e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); reveal(); } }}
                        >
                            <h3 className="font-serif">{grammar.title}</h3>
                            <p className="text-sm opacity-60">Click to reveal</p>
                        </div>
                        <div className="flashcard-face flashcard-face-back flex flex-col space-y-4">
                            <GrammarCard grammar={grammar} />
                            {grammar.example_words && grammar.example_words.length > 0 && (
                                <section className="flex flex-col space-y-4 items-baseline">
                                    <h3 className="font-serif">Example Words</h3>
                                    {grammar.example_words.map((word, index) => (
                                        <WordCard key={index} word={word} />
                                    ))}
                                </section>
                            )}
                            {grammar.example_sentences && grammar.example_sentences.length > 0 && (
                                <section className="flex flex-col space-y-4 items-baseline">
                                    <h3 className="font-serif">Example Sentences</h3>
                                    {grammar.example_sentences.map((sentence, index) => (
                                        <SentenceCard key={index} sentence={sentence} />
                                    ))}
                                </section>
                            )}
                            <ElementTagsCard element={grammar} />
                            <ElementSourcesCard element={grammar} />
                            <ElementPerformanceCard element={grammar} />
                        </div>
                    </div>
                </div>
            </section>
            {!hiddenTranslation && (
                currentIndex < grammars.length - 1 ? (
                    <button className="btn btn-primary" onClick={() => handleGoNext()}>
                        <p>Next Grammar</p>
                    </button>
                ) : (
                    <BackButton>
                        <p>Back to Lesson</p>
                    </BackButton>
                )
            )}
        </article>
    );
}
