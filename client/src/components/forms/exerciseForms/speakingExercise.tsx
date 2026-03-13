"use client";

import { useEffect, useState, useCallback } from "react";
import { Ring } from 'ldrs/react';
import 'ldrs/react/Ring.css';
import Image from 'next/image';
import Markdown from "react-markdown";
import remarkGfm from "remark-gfm";
import AudioRecorder from "@/components/audioRecorder";
import Exercise from "@/interface/features/Exercise";
import { BASE_URL, updateScoreById, evaluateSpeaking } from "@/api";

export default function SpeakingExercise({ exercise }: { exercise: Exercise }) {
    const question = exercise.question     || "";
    const answer = exercise.answer       || "";
    const text_support = exercise.text_support || "";
    const image_support = exercise.image_files  || "";
    const audio_support = exercise.audio_files  || "";

    const [isSubmitted, setIsSubmitted] = useState<boolean>(false);
    const [attempts, setAttempts] = useState<number>(0);
    const [isCorrect, setIsCorrect] = useState<boolean>(false);
    const [isLoading, setIsLoading] = useState<boolean>(false);

    // Lifted state from AudioRecorder via onStatusChange
    const [audioUrl, setAudioUrl] = useState<string | null>(null);
    const [resetKey, setResetKey] = useState<number>(0); // remounts AudioRecorder on exercise change

    const hasRecording = !!audioUrl;

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
            const result = await evaluateSpeaking(String(exercise.id), audioUrl);
            console.log("Evaluation result:", result);

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
            <h3>Speaking Exercise</h3>

            <span>
                <h3>Text to pronounce: </h3>
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
                        <Image key={index} src={`${BASE_URL}${imgSrc}`} alt="Support"
                            className="mt-2" width={300} height={300} />
                    ))}
                </span>
            )}

            {audio_support && audio_support.length > 0 && (
                <span>
                    <h3>Audio Support: </h3>
                    {audio_support.map((audioSrc, index) => (
                        <audio key={index} src={`${BASE_URL}${audioSrc}`} controls className="mt-2" />
                    ))}
                </span>
            )}

            {/* ── Recording controls ── */}
            {!isCorrect && attempts < 3 && (
                <div className="flex flex-col space-y-2">
                    <AudioRecorder
                        key={resetKey}
                        onUploadSuccess={handleUploadSuccess}
                        onUploadError={console.error}
                    />

                    {/* Submit — enabled once AudioRecorder has uploaded and returned a URL */}
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
                </div>
            )}

            {isSubmitted && (
                <div className={`mt-4 p-3 rounded-lg ${isCorrect
                    ? "bg-green-100 text-green-800"
                    : "bg-red-100 text-red-800"}`}
                >
                    {isCorrect
                        ? "✓ Correct! Well done!"
                        : `✗ Pronunciation needs work (Attempt ${attempts}/3)`
                    }

                </div>
            )}
        </div>
    );
}