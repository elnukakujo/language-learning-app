"use client";

import { useEffect, useState } from "react";
import Image from 'next/image';
import Markdown from "react-markdown";
import remarkGfm from "remark-gfm";
import shuffle from 'lodash/shuffle';

import { Ring } from 'ldrs/react';
//@ts-ignore
import 'ldrs/react/Ring.css';

import Exercise from "@/interface/features/Exercise";
import { BASE_URL, updateScoreById, evaluateText } from "@/api";
import { getLevelForScore } from "@/utils/speech_levels";

export default function OrganizeExercise({ exercise }: { exercise: Exercise }) {
    const normalize = (str: string) => str.toLowerCase();

    const question = exercise.question.split('__').map(word => normalize(word));
    const answer = exercise.answer;
    const text_support = exercise.text_support || "";
    const image_support = exercise.image_files || "";
    const audio_support = exercise.audio_files || "";

    const [attempts, setAttempts] = useState<number>(0);
    const [isCorrect, setIsCorrect] = useState<boolean>(false);
    const hasFeedback = isCorrect || attempts > 0;

    const [wordsToOrganize, setWordsToOrganize] = useState<string[]>([]);

    const [userAnswer, setUserAnswer] = useState<Array<{ word: string; sourceIndex: number }>>([]);

    const [currentLevel, setCurrentLevel] = useState<{ label: string; description: string, stars: string } | null>(null);
    const [isLoading, setIsLoading] = useState<boolean>(false);

    useEffect(() => {
        setWordsToOrganize(shuffle(question));
        setAttempts(0);
        setIsCorrect(false);
        setUserAnswer([]);
    }, [exercise]);

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        setIsLoading(true);

        evaluateText(exercise.id!, userAnswer.map(item => item.word).join(' ')).then((result) => {
            setCurrentLevel(getLevelForScore(result.score, "organize"));
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
            <h2>Organizing Exercise</h2>
            {(!isCorrect && attempts < 3) && (
                <>
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
                    <section>
                        <h3>Words to Organize:</h3>
                        <div className="flex flex-wrap space-x-2">
                            {wordsToOrganize.map((word, index) => (
                                (() => {
                                    const isSelected = userAnswer.some(item => item.sourceIndex === index);
                                    return (
                                        <button 
                                            type="button"
                                            key={index} 
                                            onClick={() => {
                                                if (isSelected) {
                                                    setUserAnswer(prev => prev.filter(item => item.sourceIndex !== index));
                                                } else {
                                                    setUserAnswer(prev => [...prev, { word, sourceIndex: index }]);
                                                }
                                            }} 
                                            className={`border p-2 rounded transition-colors ${isSelected ? 'bg-gray-200 text-gray-500 border-gray-300' : ''}`}
                                            aria-pressed={isSelected}
                                        >
                                            {word.trim()}
                                        </button>
                                    );
                                })()
                            ))}
                        </div>
                    </section>
                    <section>
                        <h3>Your answer: </h3>
                        <div className="flex flex-wrap space-x-2">
                            {userAnswer.map((item, index) => (
                                <button 
                                    type="button" 
                                    key={index} 
                                    className="border p-2 rounded cursor-pointer"
                                    onClick={() => setUserAnswer(prev => prev.filter((_, i) => i !== index))}
                                >
                                    {item.word}
                                </button>
                            ))}
                        </div>
                    </section>
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
                </>
            )}
            {hasFeedback && currentLevel && (
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
                            <p className="font-medium">Correct answer was: {answer}</p>
                        </div>  
                    )}
                </div>
            )}
        </form>
    );
}