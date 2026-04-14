"use client";

import { BASE_URL, updateScoreById } from "@/api";
import type Exercise from "@/interface/features/Exercise";
import { useEffect, useState } from "react";
import Image from 'next/image';
import Markdown from "react-markdown";
import remarkGfm from "remark-gfm";
import shuffle from 'lodash/shuffle';

export default function SelectInTheBlankExercise({ exercise }: { exercise: Exercise }) {
    const question = exercise.question || "";
    const answer = exercise.answer || "";
    const text_support = exercise.text_support || "";
    const image_support = exercise.image_files || "";
    const audio_support = exercise.audio_files || "";

    const correctAnswers = answer.split('__').map(ans => ans.trim()).filter(Boolean);

    const lines = question.split('\n').filter(line => line.trim());
    const totalBlanks = (question.match(/__/g) || []).length;

    const [wordBank, setWordBank] = useState<string[]>([]);
    const [filledAnswers, setFilledAnswers] = useState<(string | null)[]>(Array(totalBlanks).fill(null));
    const [isCorrect, setIsCorrect] = useState<boolean>(false);
    const [attempts, setAttempts] = useState(0);

    useEffect(() => {
        setWordBank(shuffle(correctAnswers));
        setFilledAnswers(Array(totalBlanks).fill(null));
        setIsCorrect(false);
        setAttempts(0);
    }, [exercise]);

    // Next unfilled blank index
    const nextBlank = filledAnswers.findIndex(a => a === null);

    const handleWordClick = (word: string, wordIdx: number) => {
        if (attempts >= 3) return; // No more attempts allowed
        if (nextBlank === -1) return;
        setFilledAnswers(prev => {
            const next = [...prev];
            next[nextBlank] = word;
            return next;
        });
        setWordBank(prev => prev.filter((_, i) => i !== wordIdx));
    };

    const handleBlankClick = (blankIdx: number) => {
        if (attempts >= 3) return; // No more attempts allowed
        if (isCorrect) return;
        const word = filledAnswers[blankIdx];
        if (!word) return;
        setFilledAnswers(prev => {
            const next = [...prev];
            next[blankIdx] = null;
            return next;
        });
        setWordBank(prev => [...prev, word]);
    };

    const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();

        if (filledAnswers.every((ans, idx) => ans === correctAnswers[idx])) {
            setIsCorrect(true);
            updateScoreById(exercise.id!, 1).catch(console.error);
        } else {
            setAttempts(prev => prev + 1);
            if (attempts >= 2) {
                updateScoreById(exercise.id!, 0).catch(console.error);
            }
        }
    };

    // Render a line with filled blanks or empty slots
    let blankCounter = 0;
    const renderLine = (line: string) => {
        const parts = line.split('__');
        return parts.flatMap((part, i, arr) => {
        if (i === arr.length - 1) return [<span key={`t-${i}`}>{part}</span>];
        const idx = blankCounter++;
        const filled = filledAnswers[idx];
        return [
            <span key={`t-${i}`}>{part}</span>,
            <button
                type="button"
                key={`blank-${idx}`}
                onClick={() => handleBlankClick(idx)}
                className={`inline-block min-w-12 mx-1 px-2 border-b-2 text-center ${isCorrect
                    ? 'border-green-500 text-green-700'
                    : ''
                } ${filled ? 'cursor-pointer' : 'cursor-default'}`}
            >
                {filled ?? '\u00A0\u00A0\u00A0\u00A0'}
            </button>
        ];
        });
    };

    return (
        <form className="flex flex-col space-y-4" onSubmit={handleSubmit}>
            <h2>Select in the Blanks Exercise</h2>
            {text_support.trim() !== "" && (
                <section>
                    <h3>Text Support:</h3>
                    <Markdown remarkPlugins={[remarkGfm]}>{text_support}</Markdown>
                </section>
            )}
            {image_support && image_support.length > 0 && (
                <section>
                    <h3>Image Support:</h3>
                    {image_support.map((imgSrc, index) => (
                        <Image key={index} src={`${BASE_URL}${imgSrc}`} alt="Support" className="mt-2" width={300} height={300} />
                    ))}
                </section>
            )}
            {audio_support && audio_support.length > 0 && (
                <section>
                    <h3>Audio Support:</h3>
                    {audio_support.map((audioSrc, index) => (
                        <audio key={index} src={`${BASE_URL}${audioSrc}`} controls className="mt-2" />
                    ))}
                </section>
            )}

            {wordBank && <section>
                <h3>Word Bank:</h3>
                <div className="flex flex-wrap gap-2">
                    {wordBank.map((word, i) => (
                        <button
                            type="button"
                            key={i}
                            onClick={() => handleWordClick(word, i)}
                            className="border px-3 py-1 rounded transition-colors"
                        >
                            {word}
                        </button>
                    ))}
                </div>
            </section>}

            <div className="flex flex-col space-y-2">
                {lines.map((line, lineIdx) => (
                <div key={lineIdx} className="flex flex-row flex-wrap items-center">
                    {renderLine(line)}
                </div>
                ))}
            </div>

            {!isCorrect && attempts < 3 && (
                <button 
                    type="submit" 
                    className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors"
                >
                    <p>Check Answers</p>
                </button>
            )}

            {attempts > 0 && (
                <div className={`mt-4 p-3 rounded-lg ${isCorrect ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
                    {isCorrect ? (
                        <>
                            <p>✓ Correct! Well done!</p>
                            <p>The correct answers are (in order):</p>
                            <div className="flex flex-row gap-2">
                                {correctAnswers.map((ans, i) => (
                                    <span key={i} className="bg-gray-100 px-2 py-1 rounded">{ans}</span>
                                ))}
                            </div>
                        </>
                    ) : (
                        <p>{`✗ Some answers are incorrect (Attempt ${attempts}/3)`}</p>
                    )}
                    {attempts >= 3 && !isCorrect && (
                        <div className="mt-2">
                            <p className="font-medium">Correct answers:</p>
                            <div className="flex gap-2 mt-1">
                                {correctAnswers.map((ans, i) => (
                                    <span key={i} className="bg-gray-100 px-2 py-1 rounded">{ans}</span>
                                ))}
                            </div>
                        </div>
                    )}
                </div>
            )}
        </form>
    );
}