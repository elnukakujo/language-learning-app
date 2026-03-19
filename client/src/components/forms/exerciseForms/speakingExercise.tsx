"use client";

import { useEffect, useState, useCallback } from "react";
import { Ring } from 'ldrs/react';
import 'ldrs/react/Ring.css';
import Image from 'next/image';
import Markdown from "react-markdown";
import remarkGfm from "remark-gfm";
import Exercise from "@/interface/features/Exercise";
import { BASE_URL, updateScoreById, evaluateSpeech } from "@/api";

import dynamic from 'next/dynamic';
const AudioRecorder = dynamic(() => import('@/components/audioRecorder'), { ssr: false });

export default function SpeakingExercise({ exercise }: { exercise: Exercise }) {
    const question = exercise.question || "";
    const text_support = exercise.text_support || "";
    const image_support = exercise.image_files || "";
    const audio_support = exercise.audio_files || "";

    const [isSubmitted, setIsSubmitted] = useState<boolean>(false);
    const [attempts, setAttempts] = useState<number>(0);
    const [isCorrect, setIsCorrect] = useState<boolean>(false);
    const [isLoading, setIsLoading] = useState<boolean>(false);
    const [currentLevel, setCurrentLevel] = useState<{ label: string; description: string } | null>(null);

    // Lifted state from AudioRecorder via onStatusChange
    const [audioUrl, setAudioUrl] = useState<string | null>(null);
    const [resetKey, setResetKey] = useState<number>(0); // remounts AudioRecorder on exercise change
    const [showExample, setShowExample] = useState<boolean>(false);

    const hasRecording = !!audioUrl;

    const speechLevels = [
        { label: "Lost in Translation", threshold: 0, description: "Your pronunciation is still finding its way—keep practicing!" },
        { label: "Tourist Mode", threshold: 0.50, description: "You're getting there, but locals might need to guess a bit." },
        { label: "Confident Speaker", threshold: 0.70, description: "You're understood, and that's a big win!" },
        { label: "Almost Native", threshold: 0.85, description: "Impressive! Just a few tweaks and you'll fool everyone." },
        { label: "Native-like", threshold: 0.95, description: "Flawless! Even locals would think you grew up here." },
    ];

    // Reset everything when the exercise changes
    useEffect(() => {
        setIsSubmitted(false);
        setAttempts(0);
        setIsCorrect(false);
        setAudioUrl(null);
        setResetKey((k) => k + 1); // remount AudioRecorder to clear its state
    }, [exercise]);

    // AudioRecorder calls this after a successful upload, giving us the server URL
    const handleUploadSuccess = useCallback((response: unknown) => {
        const res = response as { url?: string; file_url?: string };
        setAudioUrl(res.url ?? res.file_url ?? null);
    }, []);

    const handleSubmit = async () => {
        if (!audioUrl) return;
        setIsLoading(true);

        try {
            const result = await evaluateSpeech(String(exercise.id), audioUrl, 0);
            setCurrentLevel(speechLevels.sort((a, b) => b.threshold - a.threshold).find((level) => result.score >= level.threshold) || { label: "Unknown", description: "No feedback available." });

            if (result.correct) {
                setIsCorrect(true);
                updateScoreById(exercise.id!, true).catch(console.error);
            } else {
                setAttempts((prev) => prev + 1);
                if (attempts >= 2) {
                    updateScoreById(exercise.id!, false).catch(console.error);
                }
            }
            setIsSubmitted(true);

        } catch (error) {
            console.error("Error evaluating speaking:", error);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="flex flex-col space-y-4">
            <h2>Speaking Exercise</h2>
            <h3>{question}</h3>

            {text_support.trim() !== "" && (
                <span>
                    <h3>Text Support: </h3>
                    <Markdown remarkPlugins={[remarkGfm]}>{text_support}</Markdown>
                </span>
            )}

            {image_support && image_support.length > 0 && image_support.map((imgSrc, index) => (
                <Image key={index} src={`${BASE_URL}${imgSrc}`} alt="Support"
                className="mt-2" width={300} height={300} />
            ))}

            {audio_support && audio_support.length > 0 && showExample && (
                <span>
                    {audio_support.map((audioSrc, index) => (
                        <audio key={index} src={`${BASE_URL}${audioSrc}`} controls className="mt-2" />
                    ))}
                </span>
            )}

            {!isCorrect && attempts < 3 && (
                <span className="flex flex-col space-y-4">
                    <div className="flex flex-row space-x-2">
                        <button
                            type="button"
                            onClick={() => setShowExample((prev) => !prev)}
                            className="bg-gray-600 text-white px-4 py-2 rounded-lg hover:bg-gray-700 transition-colors"
                        >
                            {showExample ? "Hide Example" : "Show Example"}
                        </button>
                        <AudioRecorder
                            key={resetKey}
                            onUploadSuccess={handleUploadSuccess}
                            onUploadError={console.error}
                        />
                    </div>
                    <button
                        type="button"
                        onClick={handleSubmit}
                        disabled={!hasRecording || isLoading}
                        className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700
                                    transition-colors disabled:opacity-40 disabled:cursor-not-allowed"
                    >
                        {isLoading
                            ? <Ring size="24" stroke="2" bgOpacity="0" speed="3" color="white" />
                            : <p>Check Answer</p>
                        }
                    </button>
                </span>
            )}

            {isSubmitted && currentLevel && (
                <div className={`mt-4 p-3 rounded-lg ${isCorrect
                    ? "bg-green-100 text-green-800"
                    : "bg-red-100 text-red-800"}`}
                >
                    <h3>{currentLevel.label}</h3>
                    <p className="italic">`&quot;`{currentLevel.description}`&quot;`</p>
                </div>
            )}
        </div>
    );
}