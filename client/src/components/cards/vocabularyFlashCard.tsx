"use client";

import { updateScoreById } from "@/api";
import { useState } from "react";
import type Vocabulary from "@/interface/Vocabulary";

export default function VocabularyFlashCard({ vocabulary }: { vocabulary: Vocabulary }) {
    const [showAnswer, setShowAnswer] = useState<boolean>(false);
    const [graded, setGraded] = useState<boolean>(false);
    const [revealPhonetic, setRevealPhonetic] = useState<boolean>(false);
    const handleGrade = (isCorrect: boolean) => {
        setGraded(true);
        updateScoreById(vocabulary.id, isCorrect);
    };
    return (
        <div className="flashcard flex flex-col space-y-2">
            <h2>{vocabulary.word}{revealPhonetic && vocabulary.phonetic && ` (${vocabulary.phonetic})`}</h2>
            {vocabulary.example_sentence && <p>{vocabulary.example_sentence}</p>}
            {!showAnswer && <div className="flex flex-row space-x-4">
                <button className="bg-yellow-500 text-white rounded-md p-2" onClick={() => setRevealPhonetic(!revealPhonetic)}>
                    {revealPhonetic ? "Hide Phonetic" : "Show Phonetic"}
                </button>
                <button className="bg-blue-500 text-white rounded-md p-2" onClick={() => { setShowAnswer(!showAnswer); setRevealPhonetic(true); }}>
                    Show Answer
                </button>
            </div>}
            {showAnswer && <p>{vocabulary.translation}</p>}
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
        </div>
    );
}