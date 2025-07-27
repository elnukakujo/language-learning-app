"use client";

import { updateScoreById } from "@/api";
import { useState } from "react";
import type Vocabulary from "@/interface/Vocabulary";

export default function VocabularyFlashCard({ vocabulary }: { vocabulary: Vocabulary }) {
    const [showAnswer, setShowAnswer] = useState<boolean>(false);
    const [graded, setGraded] = useState<boolean>(false);
    const handleGrade = (isCorrect: boolean) => {
        setGraded(true);
        updateScoreById(vocabulary.id, isCorrect);
    };
    return (
        <div className="flashcard">
            <h2>{vocabulary.word}{vocabulary.phonetic && ` (${vocabulary.phonetic})`}</h2>
            <p>{vocabulary.example_sentence}</p>
            {!showAnswer && <button className="bg-blue-500 text-white rounded-md p-2" onClick={() => setShowAnswer(!showAnswer)}>
                Show Answer
            </button>}
            {showAnswer && <p>{vocabulary.translation}</p>}
            {showAnswer && !graded && (
                <>
                    <button className="bg-green-500 text-white rounded-md p-2" onClick={() => handleGrade(true)}>
                        Correct?
                    </button>
                    <button className="bg-red-500 text-white rounded-md p-2" onClick={() => handleGrade(false)}>
                        Wrong?
                    </button>
                </>
            )}
        </div>
    );
}