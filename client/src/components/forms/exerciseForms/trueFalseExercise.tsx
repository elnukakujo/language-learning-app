"use client";

import { useState, useEffect } from "react";
import Image from 'next/image';
import Markdown from "react-markdown";
import remarkGfm from "remark-gfm";

import Exercise from "@/interface/features/Exercise";
import TrueFalseInput from "@/components/input/trueFalseInput";
import { updateScoreById } from "@/api/process";
import ElementMediaCard from "@/components/cards/elementCards/elementMediaCard";

export default function TrueFalseExercise({ exercise }: {exercise: Exercise}){
    const normalize = (str: string) => str.toLowerCase().replace(/[^a-z0-9]/g, '');

    const question = exercise.question || "";
    const answer = exercise.answer || "";
    const text_support = exercise.text_support || "";
    
    const [isCorrect, setIsCorrect] = useState<boolean>(false);
        const [attempts, setAttempts] = useState<number>(0);
    const [userAnswer, setUserAnswer] = useState<boolean>(true);
        const hasFeedback = isCorrect || attempts > 0;

    useEffect(() => {
            setIsCorrect(false);
            setAttempts(0);
            setUserAnswer(true);
    }, [exercise]);

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (String(userAnswer) === normalize(answer.toLowerCase())) {
            setIsCorrect(true);
            updateScoreById(exercise.id!, 1).catch(console.error);
        } else {
            setIsCorrect(false);
            setAttempts((prev) => prev + 1);
            updateScoreById(exercise.id!, 0).catch(console.error);
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
                        className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors"
                        disabled={isCorrect}
                    >
                        Check Answers
                    </button>
                </>
            )}

            {hasFeedback && (
                <div className={`mt-4 p-3 rounded-lg ${isCorrect ? 
                    'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
                    {isCorrect ? '✓ Correct! Well done!' : `✗ Wrong answer. The correct answer was: ${answer}.`}
                </div>
            )}
        </form>
    )
}