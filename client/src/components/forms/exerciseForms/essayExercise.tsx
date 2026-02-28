"use client";

import { useEffect, useState } from "react";
import Image from 'next/image';
import Markdown from "react-markdown";
import remarkGfm from "remark-gfm";

import type Exercise from "@/interface/features/Exercise";
import { BASE_URL, updateScoreById } from "@/api";
import AutoSizeTextArea from "@/components/textArea/autoSizeTextArea";

export default function EssayExercise({ exercise }: { exercise: Exercise }) {
    const question = exercise.question || "";
    const answer = exercise.answer || "";
    const text_support = exercise.text_support || "";
    const image_support = exercise.image_files || "";
    const audio_support = exercise.audio_files || "";
    
    const [userAnswer, setUserAnswer] = useState<string>('');
    const [showCorrection, setShowCorrection] = useState<boolean>(false);

    useEffect(() => {
        setUserAnswer('');
        setShowCorrection(false);
    }, [exercise]);

    return (
        <form className="flex flex-col space-y-4">
            <h2>Essay Exercise</h2>
            <span>
                <h3>Question:</h3>
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
                className="border p-2 rounded-lg"
                placeholder="Type your answer here..."
                disabled={showCorrection}
            />
            {!showCorrection ? (
                <button
                    type="button"
                    onClick={() => {
                        setShowCorrection(true);
                        updateScoreById(exercise.id!, true).catch(console.error);
                    }}
                    className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors"
                    disabled={showCorrection}
                >
                    <p>Show Correction</p>
                </button>
            ) : null}

            {showCorrection && (
                <div className="mt-4 p-3 rounded-lg bg-gray-100 text-black">
                    <p className="font-medium">Correction:</p>
                    <p>{answer}</p>
                </div>
            )}
        </form>
    );
}