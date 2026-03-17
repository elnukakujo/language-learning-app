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
    const [revealExample, setRevealExample] = useState<boolean>(false);
    const handleGrade = (isCorrect: boolean) => {
        setGraded(true);
        updateScoreById(vocabulary.id!, isCorrect);
    };

    const handleGoNext = () => {
        setCurrentIndex(currentIndex + 1);
        setShowAnswer(false);
        setGraded(false);
        setRevealPhonetic(false);
        setRevealExample(false);
    }
    return (
        <div className="flashcard flex flex-col space-y-2">
            <h3>{currentIndex + 1} / {vocabularies.length}</h3>
            <article className="flex flex-col space-y-4">
                <section>
                    <h3>Word Information</h3>
                    <p>{vocabulary.word.word} {(vocabulary.word.phonetic || vocabulary.word.gender) && revealPhonetic && `(${[vocabulary.word.phonetic, vocabulary.word.gender].filter(v => v).join(', ')})`}</p>
                    {revealPhonetic && <p>Type: {vocabulary.word.type || "N/A"}</p>}
                    {showAnswer && <p>Translation: {vocabulary.word.translation}</p>}
                </section>
                {vocabulary.word.image_files!.length > 0 && (
                    <section className="flex flex-row space-x-4 items-center">
                        {vocabulary.word.image_files!.map((url, index) => (
                            <img
                                key={index}
                                src={BASE_URL + url}
                                alt={vocabulary.word.word}
                                width={200}
                                height={200}
                            />
                        ))}
                    </section>
                )}
                {vocabulary.word.audio_files!.length > 0 && (
                    <section className="flex flex-col space-y-4 items-baseline" >
                        {vocabulary.word.audio_files!.map((url, index) => (
                            <audio
                                key={index}
                                src={BASE_URL + url}
                                controls
                        />
                        ))}
                    </section>
                )}
                {vocabulary.example_sentences!.length > 0 && revealExample && (
                    <section className="flex flex-col space-y-4 items-baseline">
                        <h3>Example Sentences</h3>
                        {vocabulary.example_sentences!.map((sentence, index) => (
                            <article
                                key={index}
                                className="flex flex-col space-y-2 items-baseline"
                            >
                                <section>
                                    <p>{sentence.text}</p>
                                    {sentence.translation && showAnswer && <p>Sentence Translation: {sentence.translation}</p>}
                                </section>
                                {sentence.image_files!.length > 0 && (
                                    <section className="flex flex-row space-x-4 items-center">
                                        {sentence.image_files!.map((url, index) => (
                                            <img
                                                key={index}
                                                src={BASE_URL + url}
                                                alt={sentence.text}
                                                width={200}
                                                height={200}
                                            />
                                        ))}
                                    </section>
                                )}
                                {sentence.audio_files!.length > 0 && (
                                    <section className="flex flex-col space-y-4 items-baseline">
                                        {sentence.audio_files!.map((url, index) => (
                                            <audio
                                                key={index}
                                                src={BASE_URL + url}
                                                controls
                                            />
                                        ))}
                                    </section>
                                )}
                            </article>
                        ))}
                    </section>
                )}
                <section>
                    <h3>Performance Information</h3>
                    <p>Score: {vocabulary.score?.toFixed(1)}/100</p>
                    <p>Last seen: {new Date(vocabulary.last_seen || 0).toLocaleDateString('en-US')}</p>
                </section>
            </article>
            {!showAnswer && <div className="flex flex-row space-x-4">
                <button className="bg-yellow-500 text-white rounded-md p-2" onClick={() => setRevealPhonetic(!revealPhonetic)}>
                    {revealPhonetic ? "Hide Additional Information" : "Show Additional Information"}
                </button>
                {vocabulary.example_sentences && vocabulary.example_sentences.length > 0 && (
                    <button className="bg-red-500 text-white rounded-md p-2" onClick={() => setRevealExample(!revealExample)}>
                        {revealExample ? "Hide Example" : "Show Example"}
                    </button>
                )}
                <button className="bg-blue-500 text-white rounded-md p-2" onClick={() => { setShowAnswer(!showAnswer); setRevealPhonetic(true); }}>
                    Show Answer
                </button>
            </div>}
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