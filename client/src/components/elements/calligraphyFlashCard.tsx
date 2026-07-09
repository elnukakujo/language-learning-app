"use client";

import { updateScoreById } from "@/api/process";
import { useEffect, useRef, useState } from "react";
import Calligraphy from "@/interface/features/Calligraphy";
import BackButton from "@/components/ui/buttons/backButton";
import CharacterCard from "./characterCard";
import WordCard from "./wordCard";
import SentenceCard from "./sentenceCard";
import ElementTagsCard from "./elementTagsCard";
import ElementSourcesCard from "./elementSourcesCard";
import ElementPerformanceCard from "./elementPerformanceCard";

export default function CalligraphyFlashCard({ calligraphies }: { calligraphies: Calligraphy[] }) {
    const [currentIndex, setCurrentIndex] = useState<number>(0);
    const calligraphy: Calligraphy = calligraphies[currentIndex];
    const startTimeRef = useRef<number>(performance.now());
    const [hintUsed, setHintUsed] = useState<boolean>(false);

    const [hiddenTranslation, setHiddenTranslation] = useState<boolean>(true);
    const [graded, setGraded] = useState<boolean>(false);

    useEffect(() => {
        startTimeRef.current = performance.now();
        setHintUsed(false);
        setHiddenTranslation(true);
        setGraded(false);
    }, [currentIndex]);

    const handleGrade = (isCorrect: boolean) => {
        setGraded(true);
        const duration_ms = Math.round(performance.now() - startTimeRef.current);
        updateScoreById(calligraphy.id!, isCorrect ? 1 : 0, duration_ms, hintUsed);
    };

    const reveal = () => {
        if (!hiddenTranslation) return;
        setHiddenTranslation(false);
        setHintUsed(true);
    };

    const handleGoNext = () => {
        setCurrentIndex(currentIndex + 1);
    }

    return (
        <article>
            <h3>{currentIndex + 1} / {calligraphies.length}</h3>
            <section className="flex flex-col space-y-4">
                <h1>Calligraphy Sheet</h1>
                <div className="flashcard">
                    <div className={`flashcard-inner ${!hiddenTranslation ? "is-flipped" : ""}`}>
                        <div
                            className="flashcard-face card cursor-pointer flex flex-col space-y-4"
                            role="button"
                            tabIndex={0}
                            onClick={reveal}
                            onKeyDown={(e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); reveal(); } }}
                        >
                            <h3 className="font-serif">Character</h3>
                            <CharacterCard character={calligraphy.character} hiddenTranslation={true} hiddenAdditionalInformations={true} />
                            <p className="text-sm opacity-60">Click to reveal</p>
                        </div>
                        <div className="flashcard-face flashcard-face-back flex flex-col space-y-4">
                            <div className="card flex flex-col space-y-4">
                                <h3 className="font-serif">Meaning</h3>
                                <CharacterCard character={calligraphy.character} hiddenTranslation={false} hiddenAdditionalInformations={false} />
                            </div>
                            {calligraphy.example_words && (
                                <section className="flex flex-col space-y-4 items-baseline">
                                    <h3 className="font-serif">Example Words</h3>
                                    {calligraphy.example_words.map((word, index) => (
                                        <WordCard key={index} word={word} hiddenTranslation={false} hiddenAdditionalInformations={true} />
                                    ))}
                                </section>
                            )}
                            {calligraphy.example_sentences && (
                                <section className="flex flex-col space-y-4 items-baseline">
                                    <h3 className="font-serif">Example Sentences</h3>
                                    {calligraphy.example_sentences.map((sentence, index) => (
                                        <SentenceCard key={index} sentence={sentence} hiddenTranslation={false} />
                                    ))}
                                </section>
                            )}
                            <ElementTagsCard element={calligraphy} />
                            <ElementSourcesCard element={calligraphy} />
                            <ElementPerformanceCard element={calligraphy} />
                        </div>
                    </div>
                </div>
            </section>
            {!hiddenTranslation && !graded && (
                <section className="flex flex-row space-x-4">
                    <button className="btn btn-primary" onClick={() => handleGrade(true)}>
                        Correct?
                    </button>
                    <button className="btn btn-danger" onClick={() => handleGrade(false)}>
                        Wrong?
                    </button>
                </section>
            )}
            {graded && (
                currentIndex < calligraphies.length - 1 ? (
                    <button className="btn btn-primary" onClick={() => handleGoNext()}>
                        <p>Next Calligraphy</p>
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
