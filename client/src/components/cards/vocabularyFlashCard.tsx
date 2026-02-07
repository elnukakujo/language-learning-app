"use client";

import BackButton from "@/components/buttons/backButton";
import { BASE_URL, updateScoreById } from "@/api";
import { useEffect, useState } from "react";
import type Vocabulary from "@/interface/features/Vocabulary";

export default function VocabularyFlashCard({ vocabularies }: { vocabularies: Vocabulary[] }) {
    const [currentIndex, setCurrentIndex] = useState<number>(0);
    let vocabulary: Vocabulary = vocabularies[currentIndex];

    useEffect(() => {
        vocabulary = vocabularies[currentIndex];
    }, [currentIndex]);

    const [showAnswer, setShowAnswer] = useState<boolean>(false);
    const [graded, setGraded] = useState<boolean>(false);
    const [revealPhonetic, setRevealPhonetic] = useState<boolean>(false);
    const handleGrade = (isCorrect: boolean) => {
        setGraded(true);
        updateScoreById(vocabulary.id!, isCorrect);
    };

    const handleGoNext = () => {
        setCurrentIndex(currentIndex + 1);
        setShowAnswer(false);
        setGraded(false);
        setRevealPhonetic(false);
    }
    return (
        <div className="flashcard flex flex-col space-y-2">
            {vocabulary.word.image_files && vocabulary.word.image_files.length > 0 && <img
                src={BASE_URL + vocabulary.word.image_files?.[0]}
                alt={vocabulary.word.word}
                width={200}
                height={200}
            />}
            {vocabulary.word.audio_files && vocabulary.word.audio_files.length > 0 && <audio
                src={BASE_URL + vocabulary.word.audio_files?.[0]}
                controls
            />}
            <h2>{vocabulary.word.word}{revealPhonetic && vocabulary.word.phonetic && ` (${vocabulary.word.phonetic})`}</h2>

            {vocabulary.example_sentences && vocabulary.example_sentences[0] && <p>{vocabulary.example_sentences[0].text}</p>}
            {!showAnswer && <div className="flex flex-row space-x-4">
                <button className="bg-yellow-500 text-white rounded-md p-2" onClick={() => setRevealPhonetic(!revealPhonetic)}>
                    {revealPhonetic ? "Hide Phonetic" : "Show Phonetic"}
                </button>
                <button className="bg-blue-500 text-white rounded-md p-2" onClick={() => { setShowAnswer(!showAnswer); setRevealPhonetic(true); }}>
                    Show Answer
                </button>
            </div>}
            {showAnswer && <p>{vocabulary.word.translation}</p>}
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
            {graded && currentIndex < vocabularies.length - 1 && (
                <button className="bg-blue-500 text-white rounded-md p-2" onClick={() => handleGoNext()}>
                    <p>Next Vocabulary</p>
                </button>
            )}
            {graded && currentIndex === vocabularies.length - 1 && (
                <BackButton>
                    <p>Back to Unit</p>
                </BackButton>
            )}
        </div>
    );
}