"use client";

import { useState, useEffect } from "react";
import { useRef } from "react";
import Image from 'next/image';
import Markdown from "react-markdown";
import remarkGfm from "remark-gfm";

import Exercise from "@/interface/features/Exercise";
import TrueFalseInput from "@/components/exercises/trueFalseInput";
import { updateScoreById } from "@/api/process";
import ElementMediaCard from "@/components/elements/elementMediaCard";

export default function TrueFalseExercise({ exercise }: {exercise: Exercise}){
    const normalize = (str: string) => str.toLowerCase().replace(/[^a-z0-9]/g, '');

    const question = exercise.question || "";
    const answer = exercise.answer || "";
    const text_support = exercise.text_support || "";
    
    const [isCorrect, setIsCorrect] = useState<boolean>(false);
        const [attempts, setAttempts] = useState<number>(0);
    const [userAnswer, setUserAnswer] = useState<boolean>(true);
        const hasFeedback = isCorrect || attempts > 0;
    const startTimeRef = useRef<number>(performance.now());

    useEffect(() => {
            setIsCorrect(false);
            setAttempts(0);
            setUserAnswer(true);
            startTimeRef.current = performance.now();
    }, [exercise]);

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (String(userAnswer) === normalize(answer.toLowerCase())) {
            setIsCorrect(true);
            const duration_ms = Math.round(performance.now() - startTimeRef.current);
            updateScoreById(exercise.id!, 1, duration_ms, false, attempts + 1).catch(console.error);
        } else {
            const newAttempts = attempts + 1;
            setIsCorrect(false);
            setAttempts(newAttempts);
            const duration_ms = Math.round(performance.now() - startTimeRef.current);
            updateScoreById(exercise.id!, 0, duration_ms, false, newAttempts).catch(console.error);
        };
    };

    return (
        <form className="flex flex-col space-y-4">
            <h2>True or False</h2>
            <section>
                <h3>Question:</h3>
                <Markdown remarkPlugins={[remarkGfm]}>{question}</Markdown>
            </section>
            {text_support.trim() !== "" && (
                <section>
                    <h3>Text Support: </h3> 
                    <Markdown remarkPlugins={[remarkGfm]}>{text_support}</Markdown>
                </section>
            )}
            <ElementMediaCard element={exercise}/>
            {!hasFeedback && (
                <>
                    <TrueFalseInput
                        value={userAnswer}
                        onChange={(e) => setUserAnswer(e.target.value === "true")}
                    />
                    <button
                        type="button"
                        onClick={handleSubmit}
                        className="btn btn-primary"
                        disabled={isCorrect}
                    >
                        Check Answers
                    </button>
                </>
            )}

            {hasFeedback && (
                <div className={`card mt-4 ${isCorrect ?
                    'border-success/30 bg-success/10 text-success' : 'border-danger/30 bg-danger/10 text-danger'}`}>
                    {isCorrect ? '✓ Correct! Well done!' : `✗ Wrong answer. The correct answer was: ${answer}.`}
                </div>
            )}
        </form>
    )
}