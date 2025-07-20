"use client";

import { useState } from "react";

import Exercise from "@/interface/Exercise";

export default function TranslateExercise({ exercise }: {exercise: Exercise}){
    const { question, support = '', answer } = exercise;
    const normalize = (str: string) => str.toLowerCase().replace(/[^a-z0-9]/g, '');
    
    const [isSubmitted, setIsSubmitted] = useState<boolean>(false);
    const [attempts, setAttempts] = useState<number>(0);
    const [isCorrect, setIsCorrect] = useState<boolean>(false);
    const [userAnswer, setUserAnswer] = useState<string>('');

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        setIsSubmitted(true);
        if (normalize(userAnswer) === normalize(answer)) {
            setIsCorrect(true);
        } else {
            setAttempts(prev => prev + 1);
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
            <textarea 
                name="user-answer"
                value={userAnswer}
                onChange={(e) => setUserAnswer(e.target.value)}
                className={`border-2 p-2 rounded-lg ${isSubmitted && (isCorrect ? 'border-green-500' : 'border-red-500')}`}
                rows={4}
                placeholder="Type your answer here..."
            />

            {!isSubmitted || !isCorrect ? (
                <button 
                    type="button" 
                    onClick={handleSubmit}
                    className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors"
                    disabled={isSubmitted && isCorrect}
                >
                    {isSubmitted ? 'Try Again' : 'Check Answers'}
                </button>
            ) : null}

            {isSubmitted && (
                <div className={`mt-4 p-3 rounded-lg ${isCorrect ? 
                    'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
                    {isCorrect ? '✓ Correct! Well done!' : `✗ Some answers are incorrect (Attempt ${attempts}/3)`}
                    
                    {attempts >= 3 && !isCorrect && (
                    <div className="mt-2">
                        <p className="font-medium">Correct answers:</p>
                        <p>{answer}</p>
                    </div>
                    )}
                </div>
            )}
        </form>
    )
}