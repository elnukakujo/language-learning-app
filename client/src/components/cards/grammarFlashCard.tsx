"use client";

import Markdown from "react-markdown";

import type Grammar from "@/interface/Grammar";
import { useState } from "react";
import { updateScoreById } from "@/api";

export default function GrammarFlashCard({ grammar }: { grammar: Grammar }) {
    const [showAnswer, setShowAnswer] = useState<boolean>(false);
    const [graded, setGraded] = useState<boolean>(false);
    const handleGrade = (isCorrect: boolean) => {
        setGraded(true);
        updateScoreById(grammar.id, isCorrect);
    };

    return (
        <section className="flex flex-col">
            <h3>{grammar.title}</h3>
            {!showAnswer && 
                <button className="bg-blue-500 text-white rounded-md p-2" onClick={() => setShowAnswer(!showAnswer)}>
                    Show Answer
                </button>
            }
            {showAnswer && grammar.learnable_sentence && (
                <article>
                    <p className="text-sm text-gray-500">Learnable Sentence:</p>
                    <p className="text-lg font-semibold">{grammar.learnable_sentence}</p>
                </article>
            )}
            {showAnswer && !grammar.learnable_sentence && <Markdown>{grammar.explanation}</Markdown>}
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
        </section>
    );
}