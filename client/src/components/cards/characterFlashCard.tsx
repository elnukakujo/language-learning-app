"use client";

import { updateScoreById } from "@/api";
import { useState } from "react";
import type Character from "@/interface/Character";

export default function CharacterFlashCard({ character }: { character: Character }) {
    const [showAnswer, setShowAnswer] = useState<boolean>(false);
    const [graded, setGraded] = useState<boolean>(false);
    const handleGrade = (isCorrect: boolean) => {
        setGraded(true);
        updateScoreById(character.id, isCorrect);
    };
    return (
        <div className="flashcard">
            <h2>{character.character}{character.phonetic && ` (${character.phonetic})`}</h2>
            {!showAnswer && <button className="bg-blue-500 text-white rounded-md p-2" onClick={() => setShowAnswer(!showAnswer)}>
                Show Answer
            </button>}
            {showAnswer && (
                <>
                    <p>{character.components}</p>
                    {character.phonetic && <p>{character.phonetic}</p>}
                    {character.meaning && <p>{character.meaning}</p>}
                    {character.example_word && <p>{character.example_word}</p>}
                </>
            )}
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