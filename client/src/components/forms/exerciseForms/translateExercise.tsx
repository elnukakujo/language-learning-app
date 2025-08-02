"use client";

import { useState } from "react";
import Image from 'next/image';

import Exercise from "@/interface/Exercise";
import { updateScoreById } from "@/api";
import Markdown from "react-markdown";

export default function TranslateExercise({ exercise }: {exercise: Exercise}){
    const { question, support = '', answer } = exercise;
    
    const imageUrl = support.match(/<image_url>(.*?)<\/image_url>/)?.[1] || null;
    const supportText = support.replace(/<image_url>.*?<\/image_url>/, '').trim();
    
    const normalize = (str: string) => str.toLowerCase();
    
    const [isSubmitted, setIsSubmitted] = useState<boolean>(false);
    const [attempts, setAttempts] = useState<number>(0);
    const [isCorrect, setIsCorrect] = useState<boolean>(false);
    const [userAnswer, setUserAnswer] = useState<string>('');

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        setIsSubmitted(true);
        if (normalize(userAnswer) === normalize(answer)) {
            setIsCorrect(true);
            updateScoreById(exercise.id, true).catch(console.error);
        } else {
            setAttempts(prev => prev + 1);
            if (attempts >= 2) {

                updateScoreById(exercise.id, false).catch(console.error);
            }
        };
    };

    return (
        <form className="flex flex-col space-y-4">
            <h3>Translate the following sentence</h3>
            <Markdown>{question}</Markdown>
            {support && (
                <>
                    {supportText && <Markdown>{supportText}</Markdown>}
                    {imageUrl && 
                        <Image 
                            src={imageUrl} 
                            alt="Support" 
                            className="mt-2" 
                            width={300}
                            height={300}
                        />}
                </> 
            )}
            <textarea 
                name="user-answer"
                value={userAnswer}
                onChange={(e) => setUserAnswer(e.target.value)}
                className={`border-2 p-2 rounded-lg ${isSubmitted && (isCorrect ? 'border-green-500' : 'border-red-500')}`}
                rows={4}
                placeholder="Type your answer here..."
            />

            { !isCorrect && attempts < 3 ? (
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