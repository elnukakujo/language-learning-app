"use client";

import { useEffect, useState } from "react";
import { Ring } from 'ldrs/react'
import 'ldrs/react/Ring.css'
import Image from 'next/image';
import Markdown from "react-markdown";
import remarkGfm from "remark-gfm";

import Exercise from "@/interface/features/Exercise";
import AutoSizeTextArea from "@/components/textArea/autoSizeTextArea";
import { BASE_URL, updateScoreById, evaluateText } from "@/api";
import { getLevelForScore } from "@/utils/speech_levels";

export default function TranslateExercise({ exercise }: {exercise: Exercise}){
    const question = exercise.question || "";
    const answer = exercise.answer || "";
    const text_support = exercise.text_support || "";
    const image_support = exercise.image_files || "";
    const audio_support = exercise.audio_files || "";
    
    const [isSubmitted, setIsSubmitted] = useState<boolean>(false);
    const [attempts, setAttempts] = useState<number>(0);
    const [isCorrect, setIsCorrect] = useState<boolean>(false);
    const [userAnswer, setUserAnswer] = useState<string>('');

    const [currentLevel, setCurrentLevel] = useState<{ label: string; description: string, stars: string } | null>(null);

    const [isLoading, setIsLoading] = useState<boolean>(false);

    useEffect(() => {
        setIsSubmitted(false);
        setAttempts(0);
        setIsCorrect(false);
        setUserAnswer('');
    }, [exercise]);

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        setIsLoading(true);

        evaluateText(exercise.id!, userAnswer).then((result) => {
            setCurrentLevel(getLevelForScore(result.score));
            if (result.correct === true) {
                setIsCorrect(true);
                updateScoreById(exercise.id!, result.score).catch(console.error);
            } else {
                setAttempts(prev => prev + 1);
                if (attempts >= 2) {
                    updateScoreById(exercise.id!, result.score).catch(console.error);
                }
            }
            setIsLoading(false);
            setIsSubmitted(true);
        }).catch((error) => {
            setIsLoading(false);
            console.error("Error evaluating translation:", error);
        });
    };

    return (
        <form className="flex flex-col space-y-4" onSubmit={handleSubmit}>
            <h2>Translate Exercise</h2>
            <span>
                <h3>Text to translate: </h3>
                <Markdown remarkPlugins={[remarkGfm]}>{question}</Markdown>
            </span>
            {text_support.trim() !== "" && (
                <span>
                    <h3>Text Support: </h3> 
                    <Markdown remarkPlugins={[remarkGfm]}>{text_support}</Markdown>
                </span>
            )}
            {image_support && image_support.length > 0 && (
                <span>
                    <h3>Image Support: </h3>
                    {image_support.map((imgSrc, index) => (
                    <Image 
                        key={index}
                        src={`${BASE_URL}${imgSrc}`} 
                        alt="Support" 
                        className="mt-2" 
                        width={300}
                        height={300}
                    />
                    ))}
                </span>
            )}
            {audio_support && audio_support.length > 0 && (
                <span>
                    <h3>Audio Support: </h3>
                    {audio_support.map((audioSrc, index) => (
                        <audio 
                            key={index}
                            src={`${BASE_URL}${audioSrc}`}
                            controls
                            className="mt-2"
                        />
                    ))}
                </span>
            )}
            <AutoSizeTextArea
                value={userAnswer}
                onChange={(e) => setUserAnswer(e.target.value)}
                className={`border-2 p-2 rounded-lg ${isSubmitted && (isCorrect ? 'border-green-500' : 'border-red-500')}`}
                placeholder="Type your answer here..."
                disabled={isCorrect || attempts >= 3}
            />
            { !isCorrect && attempts < 3 ? (
                <button 
                    type="submit" 
                    className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors"
                    disabled={isSubmitted && isCorrect || isLoading}
                >
                    {isLoading ? (
                        <Ring
                            size="24"
                            stroke="2"
                            bgOpacity="0"
                            speed="3"
                            color="white" 
                        />
                    )
                    : (
                        <p>Check Answers</p>
                    )}
                </button>
            ) : null}

            {isSubmitted && (
                <div className={`mt-4 p-3 rounded-lg ${isCorrect ? 
                    'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
                    {isCorrect ? (
                        <>
                            <p>
                                ✓ Correct!
                            </p>
                            <p>
                                {`The correct answer is:${answer}`}
                            </p>
                        </>
                    ) : <p>✗ Some answers are incorrect (Attempt {attempts}/3)</p>}
                    <p>
                        
                        {`Level:${currentLevel!.label} (${currentLevel!.stars})`}
                    </p>
                    {attempts >= 3 && !isCorrect && (
                        <div className="mt-2">
                            <p className="font-medium">Correct answer was:</p>
                            <p>{answer}</p>
                        </div>  
                    )}
                </div>
            )}
        </form>
    )
}