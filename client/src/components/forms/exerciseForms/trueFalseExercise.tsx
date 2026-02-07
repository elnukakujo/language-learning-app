"use client";

import { useState, useEffect } from "react";
import Image from 'next/image';

import Exercise from "@/interface/features/Exercise";
import TrueFalseInput from "@/components/input/trueFalseInput";

import { BASE_URL, updateScoreById } from "@/api";
import Markdown from "react-markdown";

export default function TranslateExercise({ exercise }: {exercise: Exercise}){
    const normalize = (str: string) => str.toLowerCase().replace(/[^a-z0-9]/g, '');

    const question = exercise.question || "";
    const answer = exercise.answer || "";
    const text_support = exercise.text_support || "";
    const image_support = exercise.image_files || "";
    const audio_support = exercise.audio_files || "";
    
    const [isSubmitted, setIsSubmitted] = useState<boolean>(false);
    const [isCorrect, setIsCorrect] = useState<boolean>(false);
    const [userAnswer, setUserAnswer] = useState<boolean>(true);

    useEffect(() => {
            setIsSubmitted(false);
            setIsCorrect(false);
            setUserAnswer(true);
    }, [exercise]);

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        setIsSubmitted(true);
        if (String(userAnswer) === normalize(answer.toLowerCase())) {
            setIsCorrect(true);
            updateScoreById(exercise.id!, true).catch(console.error);
        } else {
            setIsCorrect(false);
            updateScoreById(exercise.id!, false).catch(console.error);
        };
    };

    return (
        <form className="flex flex-col space-y-4">
            <h3>Answer with true or false to the following statement:</h3>
            {question && (
                <Markdown>{question}</Markdown>
            )}
            {text_support && <Markdown>{text_support}</Markdown>}
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
            {!isSubmitted && (
                <>
                    <TrueFalseInput
                        value={userAnswer}
                        onChange={(e) => setUserAnswer(e.target.value === "true")}
                    />
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