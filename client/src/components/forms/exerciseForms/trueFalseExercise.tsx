"use client";

import { useState } from "react";

import Exercise from "@/interface/Exercise";

import { updateScoreById } from "@/api";

export default function TranslateExercise({ exercise }: {exercise: Exercise}){
    const { question, support = '', answer } = exercise;
    const normalize = (str: string) => str.toLowerCase().replace(/[^a-z0-9]/g, '');
    
    const [isSubmitted, setIsSubmitted] = useState<boolean>(false);
    const [isCorrect, setIsCorrect] = useState<boolean>(false);
    const [userAnswer, setUserAnswer] = useState<boolean>(true);

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        setIsSubmitted(true);
        if (String(userAnswer) === normalize(answer.toLowerCase())) {
            setIsCorrect(true);
            updateScoreById(exercise.id, true).catch(console.error);
        } else {
            setIsCorrect(false);
            updateScoreById(exercise.id, false).catch(console.error);
        };
    };

    return (
        <form className="flex flex-col space-y-4">
            {question && (
                <h3>{question}</h3>
            )}
            {support && (
                <p>{support}</p>
            )}
            {!isSubmitted && (
                <>
                    <div className="flex space-x-4">
                        <button
                            type="button"
                            onClick={() => setUserAnswer(true)}
                            className={`px-4 py-2 border rounded ${userAnswer ? "bg-blue-600 text-white" : "bg-gray-200 text-gray-800"}`}
                        >
                            True
                        </button>
                        <button
                            type="button"
                            onClick={() => setUserAnswer(false)}
                            className={`px-4 py-2 border rounded ${!userAnswer ? "bg-blue-600 text-white" : "bg-gray-200 text-gray-800"}`}
                        >
                            False
                        </button>
                    </div>
                    <button 
                        type="button" 
                        onClick={handleSubmit}
                        className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors"
                        disabled={isSubmitted && isCorrect}
                    >
                        {isSubmitted ? 'Try Again' : 'Check Answers'}
                    </button>
                </>
            )}

            {isSubmitted && (
                <div className={`mt-4 p-3 rounded-lg ${isCorrect ? 
                    'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
                    {isCorrect ? '✓ Correct! Well done!' : `✗ Wrong answer. The correct answer was: ${String(!userAnswer)}.`}
                </div>
            )}
        </form>
    )
}