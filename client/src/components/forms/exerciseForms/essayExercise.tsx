"use client";

import { useEffect, useState } from "react";
import Image from 'next/image';
import Markdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { Ring } from "ldrs/react";
//@ts-ignore
import 'ldrs/react/Ring.css';

import type Exercise from "@/interface/features/Exercise";
import { BASE_URL, updateScoreById, evaluateText } from "@/api";
import AutoSizeTextArea from "@/components/textArea/autoSizeTextArea";
import { getLevelForScore } from "@/utils/speech_levels";

export default function EssayExercise({ exercise }: { exercise: Exercise }) {
    const question = exercise.question || "";
    const answer = exercise.answer || "";
    const text_support = exercise.text_support || "";
    const image_support = exercise.image_files || "";
    const audio_support = exercise.audio_files || "";
    
    const [userAnswer, setUserAnswer] = useState<string>('');
    const [isCorrect, setIsCorrect] = useState<boolean>(false);
    const [isLoading, setIsLoading] = useState<boolean>(false);
    const [attempts, setAttempts] = useState<number>(0);
    const [currentLevel, setCurrentLevel] = useState<{ label: string; description: string, stars: string } | null>(null);

    useEffect(() => {
        setUserAnswer('');
        setIsCorrect(false);
        setIsLoading(false);
        setAttempts(0);
        setCurrentLevel(null);
    }, [exercise]);

    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        setIsLoading(true);

        evaluateText(exercise.id!, userAnswer).then(result => {
            setCurrentLevel(getLevelForScore(result.score, "essay"));
            if (result.correct === true) {
                setIsCorrect(true);
                updateScoreById(exercise.id!, result.score).catch(console.error);
            } else {
                const newAttempts = attempts + 1;
                setAttempts(newAttempts);
                if (newAttempts >= 3) {
                    updateScoreById(exercise.id!, result.score).catch(console.error);
                }
            }
            setIsLoading(false);
        }).catch((error) => {
            setIsLoading(false);
            console.error("Error evaluating translation:", error);
        });
    };

    return (
        <form className="flex flex-col space-y-4" onSubmit={handleSubmit}>
            <h2>Essay Exercise</h2>
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
            {image_support && image_support.length > 0 && (
                <section>
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
                </section>
            )}
            {audio_support && audio_support.length > 0 && (
                <section>
                    <h3>Audio Support: </h3>
                    {audio_support.map((audioSrc, index) => (
                        <audio 
                            key={index}
                            src={`${BASE_URL}${audioSrc}`}
                            controls
                            className="mt-2"
                        />
                    ))}
                </section>
            )}
            <AutoSizeTextArea
                value={userAnswer}
                onChange={(e) => setUserAnswer(e.target.value)}
                className="border p-2 rounded-lg"
                placeholder="Type your answer here..."
                disabled={attempts >= 3 || isCorrect || isLoading}
            />
            {(!isCorrect && attempts < 3) && (
                <button
                    type="submit"
                    className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors"
                    disabled={attempts >= 3 || isCorrect || isLoading}
                >
                    {
                        !isLoading
                        ?<p>Show Correction</p>
                        :(
                            <Ring
                                size="24"
                                stroke="2"
                                bgOpacity="0"
                                speed="3"
                                color="white" 
                            />
                        )
                    }
                </button>
            )}

            {(isCorrect || attempts > 0) && (
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
                            <p className="font-medium">The provided example answer is : {answer}</p>
                        </div>  
                    )}
                </div>
            )}
        </form>
    );
}