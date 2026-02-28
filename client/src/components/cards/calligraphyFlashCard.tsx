"use client";

import { BASE_URL, updateScoreById } from "@/api";
import { useEffect, useState } from "react";
import Calligraphy from "@/interface/features/Calligraphy";
import BackButton from "../buttons/backButton";

export default function CalligraphyFlashCard({ calligraphies }: { calligraphies: Calligraphy[] }) {
    const [currentIndex, setCurrentIndex] = useState<number>(0);
    let calligraphy: Calligraphy = calligraphies[currentIndex];

    useEffect(() => {
        calligraphy = calligraphies[currentIndex];
    }, [currentIndex]);
        
    const [showAnswer, setShowAnswer] = useState<boolean>(false);
    const [graded, setGraded] = useState<boolean>(false);
    const [revealPhonetic, setRevealPhonetic] = useState<boolean>(false);
    const [revealExample, setRevealExample] = useState<boolean>(false);

    const handleGrade = (isCorrect: boolean) => {
        setGraded(true);
        updateScoreById(calligraphy.id!, isCorrect);
    };

    const handleGoNext = () => {
        setCurrentIndex(currentIndex + 1);
        setShowAnswer(false);
        setGraded(false);
        setRevealPhonetic(false);
        setRevealExample(false);
    }

    return (
        <div className="flashcard">
            <h3>{currentIndex + 1} / {calligraphies.length}</h3>
            {calligraphy.character.image_files && calligraphy.character.image_files.length > 0 && <img
                src={BASE_URL + calligraphy.character.image_files?.[0]}
                alt={calligraphy.character.character}
                width={200}
                height={200}
            />}
            {calligraphy.character.audio_files && calligraphy.character.audio_files.length > 0 && <audio
                src={BASE_URL + calligraphy.character.audio_files?.[0]}
                controls
                autoPlay
            />}
            <h2>{calligraphy.character.character}{revealPhonetic && calligraphy.character.phonetic && ` (${calligraphy.character.phonetic})`}</h2>
            {calligraphy.character.image_files && calligraphy.character.image_files.length > 0 && <img
                src={BASE_URL + calligraphy.character.image_files?.[0]}
                alt={calligraphy.character.character}
                width={200}
                height={200}
            />}
            {revealExample &&
                <section>
                    {calligraphy.example_word!.image_files && calligraphy.example_word!.image_files.length > 0 && <img
                        src={BASE_URL + calligraphy.example_word!.image_files?.[0]}
                        alt={calligraphy.example_word!.word}
                        width={200}
                        height={200}
                    />}
                    {calligraphy.example_word!.audio_files && calligraphy.example_word!.audio_files.length > 0 && <audio
                        src={BASE_URL + calligraphy.example_word!.audio_files?.[0]}
                        controls
                        autoPlay
                    />}
                    <p>{calligraphy.example_word!.word}{calligraphy.example_word!.translation && ` (${calligraphy.example_word!.translation})`}</p>
                </section>
            }
            {showAnswer && (
                <>
                    {calligraphy.character.radical && <p>Radical: {calligraphy.character.radical}</p>}
                    {calligraphy.character.phonetic && <p>Phonetic: {calligraphy.character.phonetic}</p>}
                    {calligraphy.character.meaning && <p>Meaning: {calligraphy.character.meaning}</p>}
                </>
            )}
            {!showAnswer && <div className="flex flex-row space-x-4">
                <button className="bg-yellow-500 text-white rounded-md p-2" onClick={() => setRevealPhonetic(!revealPhonetic)}>
                    {revealPhonetic ? "Hide Phonetic" : "Show Phonetic"}
                </button>
                {calligraphy.example_word && (
                    <button className="bg-red-500 text-white rounded-md p-2" onClick={() => setRevealExample(!revealExample)}>
                        {revealExample ? "Hide Example" : "Show Example"}
                    </button>
                )}
                <button className="bg-blue-500 text-white rounded-md p-2" onClick={() => { setShowAnswer(!showAnswer); setRevealPhonetic(true); }}>
                    Show Answer
                </button>
            </div>}
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