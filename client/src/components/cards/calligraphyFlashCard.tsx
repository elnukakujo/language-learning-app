"use client";

import { BASE_URL, updateScoreById } from "@/api";
import { useEffect, useState } from "react";
import Calligraphy from "@/interface/features/Calligraphy";
import BackButton from "../buttons/backButton";
import Image from "next/image";

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
        updateScoreById(calligraphy.id!, isCorrect ? 1 : 0);
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
            <article className="flex flex-col space-y-4">
                <h1>Calligraphy Sheet</h1>
                <section>
                    <h3>Character Information</h3>
                    <p>{calligraphy.character.character} {calligraphy.character.phonetic && revealPhonetic && `(${calligraphy.character.phonetic})`} {showAnswer && calligraphy.character.meaning}</p>
                    {calligraphy.character.radical && <p>Radical: {calligraphy.character.radical}</p>}
                    {calligraphy.character.strokes && <p>Strokes: {calligraphy.character.strokes}</p>}
                </section>
                {calligraphy.character.image_files!.length > 0 && (
                    <section className="flex flex-row space-x-4 items-center">
                        {calligraphy.character.image_files!.map((url, index) => (
                            <Image
                                key={index}
                                src={BASE_URL + url}
                                alt={calligraphy.character.character}
                                width={200}
                                height={200}
                            />
                        ))}
                    </section>
                )}
                {revealPhonetic &&calligraphy.character.audio_files!.length > 0 && (
                    <section className="flex flex-col space-y-4 items-baseline" >
                        {calligraphy.character.audio_files!.map((url, index) => (
                            <audio
                                key={index}
                                src={BASE_URL + url}
                                controls
                                autoPlay
                        />
                        ))}
                    </section>
                )}
                
                {revealExample &&calligraphy.example_word && (
                    <section className="flex flex-col space-y-4 items-baseline">
                        <h3>Example Word</h3>
                        <article
                            className="flex flex-col space-y-2 items-baseline"
                        >
                            <section>
                                <p>{calligraphy.example_word.word}</p>
                                {calligraphy.example_word.translation && showAnswer && <p>Sentence Translation: {calligraphy.example_word.translation}</p>}
                            </section>
                            {calligraphy.example_word.image_files!.length > 0 && (
                                <section className="flex flex-row space-x-4 items-center">
                                    {calligraphy.example_word.image_files!.map((url, index) => (
                                        <Image
                                            key={index}
                                            src={BASE_URL + url}
                                            alt={calligraphy.example_word!.word}
                                            width={200}
                                            height={200}
                                        />
                                    ))}
                                </section>
                            )}
                            {calligraphy.example_word.audio_files!.length > 0 && revealPhonetic && (
                                <section className="flex flex-col space-y-4 items-baseline">
                                    {calligraphy.example_word.audio_files!.map((url, index) => (
                                        <audio
                                            key={index}
                                            src={BASE_URL + url}
                                            controls
                                            autoPlay
                                        />
                                    ))}
                                </section>
                            )}
                        </article>
                    </section>
                )}
                <section>
                    <h3>Performance Information</h3>
                    <p>Score: {calligraphy.score?.toFixed(1)}/100</p>
                    <p>Last seen: {new Date(calligraphy.last_seen || 0).toLocaleDateString('en-US')}</p>
                </section>
            </article>
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