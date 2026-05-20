"use client";

import { useEffect, useState } from "react";
import Markdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { Ring } from "ldrs/react";
//@ts-ignore
import 'ldrs/react/Ring.css';

import type Exercise from "@/interface/features/Exercise";
import { updateScoreById, evaluateText } from "@/api/process";
import ElementMediaCard from "@/components/cards/elementCards/elementMediaCard";
import { getLevelForScore } from "@/utils/speech_levels";
import AutoSizeTextArea from "@/components/textArea/autoSizeTextArea";

export default function AnsweringExercise({ exercise }: { exercise: Exercise }) {
    const question = exercise.question || "";
    const answer = exercise.answer || "";
    const text_support = exercise.text_support || "";
    
    const [userAnswer, setUserAnswer] = useState<string>('');

    const [isCorrect, setIsCorrect] = useState<boolean>(false);
    const [attempts, setAttempts] = useState<number>(0);
    const [currentLevel, setCurrentLevel] = useState<{ label: string; description: string, stars: string } | null>(null);
    const [isLoading, setIsLoading] = useState<boolean>(false);
    const [feedbackMessage, setFeedbackMessage] = useState<string | null>(null);
    const hasFeedback = isCorrect || attempts > 0;

    useEffect(() => {
        setUserAnswer('');
        setCurrentLevel(null);
        setIsLoading(false);
        setIsCorrect(false);
        setAttempts(0);
        setFeedbackMessage(null);
    }, [exercise]);

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        setIsLoading(true);

        evaluateText(exercise.id!, userAnswer).then((result) => {
            setFeedbackMessage(result.feedback);
            setCurrentLevel(getLevelForScore(result.score, "answering"));
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
            setFeedbackMessage(null);
            setIsLoading(false);
            console.error("Error evaluating answer:", error);
        });
    };

    return (
        <form className="flex flex-col space-y-2" onSubmit={handleSubmit}>
            <h2>Answering Exercise</h2>
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
            <AutoSizeTextArea
                value={userAnswer}
                onChange={(e) => setUserAnswer(e.target.value)}
                className="border p-2 rounded-lg"
                disabled={isLoading || isCorrect || attempts >= 3}
            />
            { !isCorrect && attempts < 3 ? (
                <button 
                    type="submit" 
                    className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors"
                    disabled={isCorrect || attempts >= 3 || isLoading}
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

            {hasFeedback && currentLevel && (
                <div className={`mt-4 p-3 rounded-lg ${isCorrect ? 
                    'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
                    {isCorrect ? (
                        <>
                            <p>
                                {feedbackMessage && (
                                    <span className="font-medium">Feedback: </span>
                                )}
                                {feedbackMessage}
                            </p>
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
                            <p className="font-medium">Correct answer was: {answer}</p>
                        </div>  
                    )}
                </div>
            )}
        </form>
    );
}