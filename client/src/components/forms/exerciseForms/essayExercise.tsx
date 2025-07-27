"use client";

import { useState } from "react";
import Image from 'next/image';

import type Exercise from "@/interface/Exercise";
import { updateScoreById } from "@/api";

export default function EssayExercise({ exercise }: { exercise: Exercise }) {
    const { question, support = '', answer } = exercise;

    const imageUrl = support.match(/<image_url>(.*?)<\/image_url>/)?.[1] || null;
    const supportText = support.replace(/<image_url>.*?<\/image_url>/, '').trim();

    const [userAnswer, setUserAnswer] = useState<string>('');
    const [showCorrection, setShowCorrection] = useState<boolean>(false);

    return (
        <form className="flex flex-col space-y-4">
            {question && <h3>{question}</h3>}
            {support && (
                <>
                    {supportText && <p>{supportText}</p>}
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
                className="border p-2 rounded-lg"
                rows={5}
                disabled={showCorrection}
            />
            {!showCorrection ? (
                <button
                    type="button"
                    onClick={() => {
                        setShowCorrection(true);
                        updateScoreById(exercise.id, true).catch(console.error);
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