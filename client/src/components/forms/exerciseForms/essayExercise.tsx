"use client";

import { useState } from "react";
import Image from 'next/image';
import Markdown from "react-markdown";

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

    return (
        <form className="flex flex-col space-y-4">
            {question && <Markdown>{question}</Markdown>}
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