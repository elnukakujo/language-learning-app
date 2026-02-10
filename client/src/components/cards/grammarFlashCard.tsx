"use client";

import type Grammar from "@/interface/features/Grammar";
import { useEffect, useState } from "react";
import { BASE_URL, updateScoreById } from "@/api";
import BackButton from "../buttons/backButton";

export default function GrammarFlashCard({ grammars }: { grammars: Grammar[] }) {
    const [currentIndex, setCurrentIndex] = useState<number>(0);
    let grammar: Grammar = grammars[currentIndex];

    useEffect(() => {
        grammar = grammars[currentIndex];
    }, [currentIndex]);

    const [showAnswer, setShowAnswer] = useState<boolean>(false);
    const [graded, setGraded] = useState<boolean>(false);
    const handleGrade = (isCorrect: boolean) => {
        setGraded(true);
        updateScoreById(grammar.id!, isCorrect);
    };

    const handleGoNext = () => {
        setCurrentIndex(currentIndex + 1);
        setShowAnswer(false);
        setGraded(false);
    }

    return (
        <section className="flex flex-col">
            <h3>{currentIndex + 1} / {grammars.length}</h3>

            <h3>{grammar.title}</h3>
            {grammar.learnable_sentences![0].image_files && grammar.learnable_sentences![0].image_files.length > 0 && <img
                src={BASE_URL + grammar.learnable_sentences![0].image_files?.[0]}
                alt={grammar.learnable_sentences![0].text}
                width={200}
                height={200}
            />}
            {!showAnswer && 
                <button className="bg-blue-500 text-white rounded-md p-2" onClick={() => setShowAnswer(!showAnswer)}>
                    Show Answer
                </button>
            }
            {showAnswer && grammar.learnable_sentences && grammar.learnable_sentences[0] && (
                <article>
                    <h4 className="text-sm text-gray-500">Learnable Sentence:</h4>
                    {grammar.learnable_sentences![0].audio_files && grammar.learnable_sentences![0].audio_files.length > 0 && <audio
                        src={BASE_URL + grammar.learnable_sentences![0].audio_files?.[0]}
                        controls
                        autoPlay
                    />}
                    <p className="text-lg font-semibold">{grammar.learnable_sentences[0].text}{grammar.learnable_sentences[0].translation && ` (${grammar.learnable_sentences[0].translation})`}</p>
                </article>
            )}
            {showAnswer && !graded && (
                <div className="flex flex-row space-x-4">
                    <button className="bg-green-500 text-white rounded-md p-2" onClick={() => handleGrade(true)}>
                        Correct?
                    </button>
                    <button className="bg-red-500 text-white rounded-md p-2" onClick={() => handleGrade(false)}>
                        Wrong?
                    </button>
                </div>
            )}
            {graded && currentIndex < grammars.length - 1 && (
                <button className="bg-blue-500 text-white rounded-md p-2" onClick={() => handleGoNext()}>
                    <p>Next Grammar Sentence</p>
                </button>
            )}
            {graded && currentIndex === grammars.length - 1 && (
                <BackButton>
                    <p>Back to Unit</p>
                </BackButton>
            )}
        </section>
    );
}