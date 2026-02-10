"use client";

import { useEffect, useState } from "react";
import Image from 'next/image';
import Markdown from "react-markdown";
import remarkGfm from "remark-gfm";

import Exercise from "@/interface/features/Exercise";
import AutoSizeTextArea from "@/components/textArea/autoSizeTextArea";
import { BASE_URL, updateScoreById } from "@/api";

export default function TranslateExercise({ exercise }: {exercise: Exercise}){
    const question = exercise.question || "";
    const answer = exercise.answer || "";
    const text_support = exercise.text_support || "";
    const image_support = exercise.image_files || "";
    const audio_support = exercise.audio_files || "";
    
    const normalize = (str: string) => str.toLowerCase();
    
    const [isSubmitted, setIsSubmitted] = useState<boolean>(false);
    const [attempts, setAttempts] = useState<number>(0);
    const [isCorrect, setIsCorrect] = useState<boolean>(false);
    const [userAnswer, setUserAnswer] = useState<string>('');

    useEffect(() => {
        setIsSubmitted(false);
        setAttempts(0);
        setIsCorrect(false);
        setUserAnswer('');
    }, [exercise]);

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        setIsSubmitted(true);
        if (normalize(userAnswer) === normalize(answer)) {
            setIsCorrect(true);
            updateScoreById(exercise.id!, true).catch(console.error);
        } else {
            setAttempts(prev => prev + 1);
            if (attempts >= 2) {

                updateScoreById(exercise.id!, false).catch(console.error);
            }
        };
    };

    return (
        <form className="flex flex-col space-y-4">
            <h3>Translate the following sentence</h3>
            <Markdown remarkPlugins={[remarkGfm]}>{question}</Markdown>
            {text_support && <Markdown remarkPlugins={[remarkGfm]}>{text_support}</Markdown>}
            {image_support && image_support.map((imgSrc, index) => (
                <Image 
                    key={index}
                    src={`${BASE_URL}${imgSrc}`} 
                    alt="Support" 
                    className="mt-2" 
                    width={300}
                    height={300}
                />
            ))}
            {audio_support && audio_support.map((audioSrc, index) => (
                <audio 
                    key={index}
                    src={`${BASE_URL}${audioSrc}`}
                    controls
                    className="mt-2"
                />
            ))}
            <AutoSizeTextArea
                value={userAnswer}
                onChange={(e) => setUserAnswer(e.target.value)}
                className={`border-2 p-2 rounded-lg ${isSubmitted && (isCorrect ? 'border-green-500' : 'border-red-500')}`}
                placeholder="Type your answer here..."
                disabled={isCorrect || attempts >= 3}
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