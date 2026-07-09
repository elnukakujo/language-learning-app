"use client";

import { updateScoreById } from "@/api/process";
import type Exercise from "@/interface/features/Exercise";
import { useEffect, useState } from "react";
import { useRef } from "react";
import Markdown from "react-markdown";
import remarkGfm from "remark-gfm";
import shuffle from 'lodash/shuffle';
import ElementMediaCard from "@/components/elements/elementMediaCard";

export default function SelectInTheBlankExercise({ exercise }: { exercise: Exercise }) {
    const question = exercise.question || "";
    const answer = exercise.answer || "";
    const text_support = exercise.text_support || "";

    const correctAnswers = answer.split('__').map(ans => ans.trim()).filter(Boolean);

    const lines = question.split('\n').filter(line => line.trim());
    const totalBlanks = (question.match(/__/g) || []).length;

    const [wordBank, setWordBank] = useState<string[]>([]);
    const [filledAnswers, setFilledAnswers] = useState<(string | null)[]>(Array(totalBlanks).fill(null));
    const [isCorrect, setIsCorrect] = useState<boolean>(false);
    const [attempts, setAttempts] = useState(0);
    const startTimeRef = useRef<number>(performance.now());

    useEffect(() => {
        setWordBank(shuffle(correctAnswers));
        setFilledAnswers(Array(totalBlanks).fill(null));
        setIsCorrect(false);
        setAttempts(0);
        startTimeRef.current = performance.now();
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
            const duration_ms = Math.round(performance.now() - startTimeRef.current);
            updateScoreById(exercise.id!, 1, duration_ms, false, attempts + 1).catch(console.error);
        } else {
            const newAttempts = attempts + 1;
            setAttempts(newAttempts);
            if (attempts >= 2) {
                const duration_ms = Math.round(performance.now() - startTimeRef.current);
                updateScoreById(exercise.id!, 0, duration_ms, false, newAttempts).catch(console.error);
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
                    ? 'border-success text-success'
                    : 'border-border'
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
            <ElementMediaCard element={exercise}/>

            {wordBank && <section>
                <h3>Word Bank:</h3>
                <div className="flex flex-wrap gap-2">
                    {wordBank.map((word, i) => (
                        <button
                            type="button"
                            key={i}
                            onClick={() => handleWordClick(word, i)}
                            className="btn btn-secondary"
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
                    className="btn btn-primary"
                >
                    <p>Check Answers</p>
                </button>
            )}

            {attempts > 0 && (
                <div className={`card mt-4 ${isCorrect ? 'border-success/30 bg-success/10 text-success' : 'border-danger/30 bg-danger/10 text-danger'}`}>
                    {isCorrect ? (
                        <>
                            <p>✓ Correct! Well done!</p>
                            <p>The correct answers are (in order):</p>
                            <div className="flex flex-row gap-2">
                                {correctAnswers.map((ans, i) => (
                                    <span key={i} className="badge">{ans}</span>
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
                                    <span key={i} className="badge">{ans}</span>
                                ))}
                            </div>
                        </div>
                    )}
                </div>
            )}
        </form>
    );
}