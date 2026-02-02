"use client";

import { updateScoreById } from "@/api";
import { useEffect, useState } from "react";
import Calligraphy from "@/interface/features/Calligraphy";
import BackButton from "../buttons/backButton";

export default function CalligraphyFlashCard({ calligraphies }: { calligraphies: Calligraphy[] }) {
    const [currentIndex, setCurrentIndex] = useState<number>(0);
    let calligraphy: Calligraphy = calligraphies[currentIndex];

    useEffect(() => {
        calligraphy = calligraphies[currentIndex];
        console.log("Current Calligraphy:", calligraphy);
    }, [currentIndex]);
        
    const [showAnswer, setShowAnswer] = useState<boolean>(false);
    const [graded, setGraded] = useState<boolean>(false);
    const handleGrade = (isCorrect: boolean) => {
        setGraded(true);
        updateScoreById(calligraphy.id!, isCorrect);
    };

    const handleGoNext = () => {
        setCurrentIndex(currentIndex + 1);
        setShowAnswer(false);
        setGraded(false);
    }

    return (
        <div className="flashcard">
            <h2>{calligraphy.character.character}</h2>
            {!showAnswer && <button className="bg-blue-500 text-white rounded-md p-2" onClick={() => setShowAnswer(!showAnswer)}>
                Show Answer
            </button>}
            {showAnswer && (
                <>
                    {calligraphy.character.radical && <p>Radical: {calligraphy.character.radical}</p>}
                    {calligraphy.character.phonetic && <p>Phonetic: {calligraphy.character.phonetic}</p>}
                    {calligraphy.character.meaning && <p>Meaning: {calligraphy.character.meaning}</p>}
                    {calligraphy.example_word && <p>Example: {calligraphy.example_word.word}</p>}
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
            {graded && currentIndex < calligraphies.length - 1 && (
                <button className="bg-blue-500 text-white rounded-md p-2" onClick={() => handleGoNext()}>
                    <p>Next Calligraphy</p>
                </button>
            )}
            {graded && currentIndex === calligraphies.length - 1 && (
                <BackButton>
                    <p>Back to Unit</p>
                </BackButton>
            )}
        </div>
    );
}