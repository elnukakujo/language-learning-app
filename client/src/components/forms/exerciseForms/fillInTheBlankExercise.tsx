"use client";

import { BASE_URL, updateScoreById } from "@/api";
import type Exercise from "@/interface/features/Exercise";
import { useEffect, useState } from "react";
import Image from 'next/image';
import Markdown from "react-markdown";
import remarkGfm from "remark-gfm";
import shuffle from 'lodash/shuffle';
import AutoWidthInput from "@/components/input/autoWidthInput";

export default function FillInTheBlankExercise({ exercise }: { exercise: Exercise }) {
    const question = exercise.question || "";
    const answer = exercise.answer || "";
    const text_support = exercise.text_support || "";
    const image_support = exercise.image_files || "";
    const audio_support = exercise.audio_files || "";

    const normalize = (str: string) => str.toLowerCase().trim();

    const correctAnswers = answer.split('__').map(a => a.trim()).filter(Boolean);
    const lines = question.split('\n').filter(line => line.trim());
    const totalBlanks = (question.match(/__/g) || []).length;

    const [isAssisted, setIsAssisted] = useState<boolean>(totalBlanks > 3); // Auto-enable word bank for 4+ blanks

    const [wordBank, setWordBank] = useState<string[]>([]);
    const [filledAnswers, setFilledAnswers] = useState<(string | null)[]>(Array(totalBlanks).fill(null));
    const [isSubmitted, setIsSubmitted] = useState(false);
    const [isCorrect, setIsCorrect] = useState<boolean[]>(Array(totalBlanks).fill(false));
    const [attempts, setAttempts] = useState(0);

    useEffect(() => {
        setIsAssisted(totalBlanks > 3);
        if (isAssisted) {
            setWordBank(shuffle(correctAnswers));
        }
        setFilledAnswers(Array(totalBlanks).fill(null));
        setIsSubmitted(false);
        setIsCorrect(Array(totalBlanks).fill(false));
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
        if (isSubmitted && isCorrect[blankIdx]) return;
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
        setIsSubmitted(true);
        const newIsCorrect = filledAnswers.map((ans, i) =>
            normalize(ans ?? '') === normalize(correctAnswers[i] ?? '')
        );
        setIsCorrect(newIsCorrect);

        if (newIsCorrect.every(Boolean)) {
            updateScoreById(exercise.id!, true).catch(console.error);
        } else {
            const newAttempts = attempts + 1;
            setAttempts(newAttempts);
            if (newAttempts >= 3) {
                updateScoreById(exercise.id!, false).catch(console.error);
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

            (isAssisted ? (
                <button
                    type="button"
                    key={`blank-${idx}`}
                    onClick={() => handleBlankClick(idx)}
                    className={`inline-block min-w-12 mx-1 px-2 border-b-2 text-center ${
                        isSubmitted
                        ? isCorrect[idx]
                            ? 'border-green-500 text-green-700'
                            : 'border-red-500 text-red-700'
                        : 'border-gray-400'
                    } ${filled ? 'cursor-pointer' : 'cursor-default'}`}
                >
                    {filled ?? '\u00A0\u00A0\u00A0\u00A0'}
                </button>
            ) : (
                <AutoWidthInput
                    key={`blank-${idx}`}
                    value={filledAnswers[idx] ?? ''}
                    onChange={(e) => {
                        if (attempts >= 3) return;
                        const val = e.target.value;
                        setFilledAnswers(prev => {
                            const next = [...prev];
                            next[idx] = val;
                            return next;
                        });
                    }}
                    disabled={isSubmitted}
                    className={`inline-block mx-1 border-b-2 text-center ${
                        isSubmitted
                        ? isCorrect[idx]
                            ? 'border-green-500 text-green-700'
                            : 'border-red-500 text-red-700'
                        : 'border-gray-400'
                    }`}
                />
            )),
        ];
        });
    };

    return (
        <form className="flex flex-col space-y-4" onSubmit={handleSubmit}>
            <h2>Fill the Blanks Exercise</h2>
            {text_support.trim() !== "" && (
                <span>
                    <h3>Text Support:</h3>
                    <Markdown remarkPlugins={[remarkGfm]}>{text_support}</Markdown>
                </span>
            )}
            {image_support && image_support.length > 0 && (
                <span>
                    <h3>Image Support:</h3>
                    {image_support.map((imgSrc, index) => (
                        <Image key={index} src={`${BASE_URL}${imgSrc}`} alt="Support" className="mt-2" width={300} height={300} />
                    ))}
                </span>
            )}
            {audio_support && audio_support.length > 0 && (
                <span>
                    <h3>Audio Support:</h3>
                    {audio_support.map((audioSrc, index) => (
                        <audio key={index} src={`${BASE_URL}${audioSrc}`} controls className="mt-2" />
                    ))}
                </span>
            )}

            {isAssisted && wordBank && (
                <span>
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
                </span>
            )}

            <div className="flex flex-col space-y-2">
                {lines.map((line, lineIdx) => (
                <div key={lineIdx} className="flex flex-row flex-wrap items-center">
                    {renderLine(line)}
                </div>
                ))}
            </div>

            {!isCorrect.every(Boolean) && attempts < 3 && (
                <button 
                    type="submit" 
                    className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors"
                >
                    Check Answers
                </button>
            )}

            {isSubmitted && (
                <div className={`mt-4 p-3 rounded-lg ${isCorrect.every(Boolean) ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
                    {isCorrect.every(Boolean)
                        ? '✓ Correct! Well done!'
                        : `✗ Some answers are incorrect (Attempt ${attempts}/3)`}
                    {attempts >= 3 && !isCorrect.every(Boolean) && (
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