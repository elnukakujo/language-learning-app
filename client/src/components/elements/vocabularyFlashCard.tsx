"use client";

import BackButton from "@/components/ui/buttons/backButton";
import { updateScoreById } from "@/api/process";
import { useEffect, useRef, useState } from "react";
import type Vocabulary from "@/interface/features/Vocabulary";
import WordCard from "./wordCard";
import SentenceCard from "./sentenceCard";
import ElementPerformanceCard from "./elementPerformanceCard";
import ElementSourcesCard from "./elementSourcesCard";
import ElementTagsCard from "./elementTagsCard";

export default function VocabularyFlashCard({ vocabularies }: { vocabularies: Vocabulary[] }) {
    const [currentIndex, setCurrentIndex] = useState<number>(0);
    const vocabulary: Vocabulary = vocabularies[currentIndex];
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
        updateScoreById(vocabulary.id!, isCorrect ? 1 : 0, duration_ms, hintUsed);
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
            <h3>{currentIndex + 1} / {vocabularies.length}</h3>
            <section className="flex flex-col space-y-4">
                <h1>Vocabulary Sheet</h1>
                <div className="flashcard">
                    <div className={`flashcard-inner ${!hiddenTranslation ? "is-flipped" : ""}`}>
                        <div
                            className="flashcard-face card cursor-pointer flex flex-col space-y-4"
                            role="button"
                            tabIndex={0}
                            onClick={reveal}
                            onKeyDown={(e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); reveal(); } }}
                        >
                            <WordCard word={vocabulary.word} hiddenTranslation={true} hiddenAdditionalInformations={true} />
                            <p className="text-sm opacity-60">Click to reveal</p>
                        </div>
                        <div className="flashcard-face flashcard-face-back flex flex-col space-y-4">
                            <div className="card flex flex-col space-y-4">
                                <h3 className="font-serif">Translation</h3>
                                <WordCard word={vocabulary.word} hiddenTranslation={false} hiddenAdditionalInformations={false} />
                            </div>
                            {vocabulary.example_sentences && (
                                <section className="flex flex-col space-y-4 items-baseline">
                                    <h3 className="font-serif">Example Sentences</h3>
                                    {vocabulary.example_sentences.map((sentence, index) => (
                                        <SentenceCard key={index} sentence={sentence} hiddenTranslation={false} />
                                    ))}
                                </section>
                            )}
                            <ElementTagsCard element={vocabulary} />
                            <ElementSourcesCard element={vocabulary} />
                            <ElementPerformanceCard element={vocabulary} />
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
                currentIndex < vocabularies.length - 1 ? (
                    <button className="btn btn-primary" onClick={() => handleGoNext()}>
                        <p>Next Vocabulary</p>
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
