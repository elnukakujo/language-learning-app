"use client";

import { useState } from "react";
import Exercise from "@/interface/Exercise";
import { updateScoreById } from "@/api";

export default function OrganizeExercise({ exercise }: { exercise: Exercise }) {
    const { question, support = '', answer } = exercise;
    const [attempts, setAttempts] = useState<number>(0);
    const [isCorrect, setIsCorrect] = useState<boolean>(false);

    const normalize = (str: string) => str.toLowerCase().replace(/[^a-z0-9]/g, '');

    const wordsToOrganize = question.split('/').map(word => normalize(word));
    const [userAnswer, setUserAnswer] = useState<string[]>([]);

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        console.log("submit")
        if (userAnswer.join(' ') === answer.split(' ').map(word => normalize(word)).filter(word => word.length > 1).join(' ')) {
            setIsCorrect(true);
            updateScoreById(exercise.id, true).catch(console.error);
        } else {
            setAttempts(prev => prev + 1);
            if (attempts >= 2) {
                updateScoreById(exercise.id, false).catch(console.error);
            }
        }
    };

    return (
        <form className="flex flex-col space-y-4" onSubmit={handleSubmit}>
            <h3>Organize the following word/characters sequence</h3>
            {(!isCorrect && attempts < 3) && (
                <>
                    <div className="flex flex-wrap space-x-2">
                        {wordsToOrganize.map((word, index) => (
                            <button 
                                type="button"
                                key={index} 
                                onClick={() => setUserAnswer(prev => [...prev, word])} 
                                className="border p-2 rounded"
                            >
                                {word.trim()}
                            </button>
                        ))}
                    </div>
                    <label htmlFor="userAnswer">Your Answer:</label>
                    <div className="flex flex-wrap space-x-2">
                        {userAnswer.map((word, index) => (
                            <button 
                                type="button" 
                                key={index} 
                                className="border p-2 rounded cursor-pointer"
                                onClick={() => setUserAnswer(prev => prev.filter((_, i) => i !== index))}
                            >
                                {word}
                            </button>
                        ))}
                    </div>
                    <button 
                        type="submit" 
                        className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors"
                    >
                        Check Answers
                    </button>
                </>
            )}
            {(attempts>0 || isCorrect) && (
                <div className={`mt-4 p-3 rounded-lg ${isCorrect ? 
                    'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
                    <p>{isCorrect ? '✓ Correct! Well done!' : `✗ Some answers are incorrect (Attempt ${attempts}/3)`}</p>

                    {attempts >= 3 && !isCorrect && (
                    <div className="mt-2">
                        <p className="font-medium">Correct answers:</p>
                        <p className="flex gap-2 mt-1">
                            {answer.split(' ').map(word => normalize(word)).filter(word => word.length > 1).join(' ')}
                        </p>
                    </div>
                    )}
                </div>
            )}
        </form>
    );
}