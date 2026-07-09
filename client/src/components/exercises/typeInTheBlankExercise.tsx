"use client";

import { evaluateText, updateScoreById } from "@/api/process";
import type Exercise from "@/interface/features/Exercise";
import { useEffect, useState } from "react";
import { useRef } from "react";
import Image from 'next/image';
import Markdown from "react-markdown";
import remarkGfm from "remark-gfm";
import AutoWidthInput from "@/components/ui/input/autoWidthInput";
import { getLevelForScore } from "@/utils/speech_levels";
import { Ring } from 'ldrs/react';
//@ts-ignore
import 'ldrs/react/Ring.css';
import ElementMediaCard from "@/components/elements/elementMediaCard";

export default function TypeInTheBlankExercise({ exercise }: { exercise: Exercise }) {
    const question = exercise.question || "";
    const answer = exercise.answer || "";
    const text_support = exercise.text_support || "";

    const lines = question.split('\n').filter(line => line.trim());
    const totalBlanks = (question.match(/__/g) || []).length;
    const questionParts = question.split('__');
    const correctAnswers = questionParts.slice(0, -1).map((part, index) => {
        const nextPart = questionParts[index + 1] || "";
        const start = answer.indexOf(part) + part.length;
        const end = nextPart ? answer.indexOf(nextPart, start) : answer.length;

        if (start < part.length || end < start) {
            return "";
        }

        return answer.slice(start, end).trim();
    }).filter(Boolean);

    const [filledAnswers, setFilledAnswers] = useState<(string | null)[]>(Array(totalBlanks).fill(null));
    const [isCorrect, setIsCorrect] = useState<boolean>(false);
    const [attempts, setAttempts] = useState(0);
    const hasFeedback = isCorrect || attempts > 0;
    const [currentLevel, setCurrentLevel] = useState<{ label: string; description: string, stars: string } | null>(null);
    const [isLoading, setIsLoading] = useState<boolean>(false);
    const [feedbackMessage, setFeedbackMessage] = useState<string | null>(null);
    const startTimeRef = useRef<number>(performance.now());

    useEffect(() => {
        setFilledAnswers(Array(totalBlanks).fill(null));
        setIsCorrect(false);
        setAttempts(0);
        setCurrentLevel(null);
        setIsLoading(false);
        setFeedbackMessage(null);
        startTimeRef.current = performance.now();
    }, [exercise]);

    const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        setIsLoading(true);

        let answerIndex = 0;
        const userText = question.replace(/__/g, () => {
            const nextAnswer = filledAnswers[answerIndex++] ?? "";
            return (nextAnswer ?? "").trim();
        });

        evaluateText(exercise.id!, userText).then((result) => {
            setFeedbackMessage(result.feedback);
            setCurrentLevel(getLevelForScore(result.score, "type_in_the_blank"));
            if (result.correct === true) {
                setIsCorrect(true);
                const duration_ms = Math.round(performance.now() - startTimeRef.current);
                updateScoreById(exercise.id!, result.score, duration_ms, false, attempts + 1).catch(console.error);
            } else {
                const newAttempts = attempts + 1;
                setAttempts(newAttempts);
                if (newAttempts >= 3) {
                    const duration_ms = Math.round(performance.now() - startTimeRef.current);
                    updateScoreById(exercise.id!, result.score, duration_ms, false, newAttempts).catch(console.error);
                }
            }
            setIsLoading(false);
        }).catch((error) => {
            setFeedbackMessage(null);
            setIsLoading(false);
            console.error("Error evaluating fill-in-the-blank:", error);
        });
    };

    // Render a line with filled blanks or empty slots
    let blankCounter = 0;
    const renderLine = (line: string) => {
        const parts = line.split('__');
        return parts.flatMap((part, i, arr) => {
        if (i === arr.length - 1) return [<span key={`t-${i}`}>{part}</span>];
        const idx = blankCounter++;
        return [
            <span key={`t-${i}`}>{part}</span>,
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
                disabled={isCorrect || attempts >= 3}
                className={`inline-block mx-1 border-b-2 text-center ${
                    hasFeedback
                    ? isCorrect
                        ? 'border-success text-success'
                        : 'border-danger text-danger'
                    : 'border-border'
                }`}
            />
            ];
        });
    };

    return (
        <form className="flex flex-col space-y-4" onSubmit={handleSubmit}>
            <h2>Type the Blanks Exercise</h2>
            {text_support.trim() !== "" && (
                <section>
                    <h3>Text Support:</h3>
                    <Markdown remarkPlugins={[remarkGfm]}>{text_support}</Markdown>
                </section>
            )}
            <ElementMediaCard element={exercise}/>

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
                    disabled={isLoading}
                >
                    {isLoading ? (
                        <Ring
                            size="24"
                            stroke="2"
                            bgOpacity="0"
                            speed="3"
                            color="white"
                        />
                    ) : (
                        <p>Check Answers</p>
                    )}
                </button>
            )}

            {hasFeedback && (
                <div className={`card mt-4 ${isCorrect ? 'border-success/30 bg-success/10 text-success' : 'border-danger/30 bg-danger/10 text-danger'}`}>
                    {isCorrect ? (
                        <>
                            <p>✓ Correct! Well done!</p>
                            <p>{`The correct answer is:${answer}`}</p>
                        </>
                    ) : (
                        <p>{`✗ Some answers are incorrect (Attempt ${attempts}/3)`}</p>
                    )}
                    <p>
                        {feedbackMessage && (
                            <span className="font-medium">Feedback: </span>
                        )}
                        {feedbackMessage}
                    </p>
                    {currentLevel && <p>{`Level:${currentLevel.label} (${currentLevel.stars})`}</p>}
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