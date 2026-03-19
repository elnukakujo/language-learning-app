"use client";

import { useEffect, useState } from "react";
import { Ring } from 'ldrs/react';
import 'ldrs/react/Ring.css';
import Markdown from "react-markdown";
import remarkGfm from "remark-gfm";
import Image from 'next/image';
import Exercise from "@/interface/features/Exercise";
import { BASE_URL, updateScoreById, evaluateSpeech } from "@/api";

import dynamic from 'next/dynamic';
const AudioRecorder = dynamic(() => import('@/components/audioRecorder'), { ssr: false });

// ─── Types ────────────────────────────────────────────────────────────────────

type Speaker = {
    id: string;
    name: string;
    isUser: boolean;
};

type ConversationLine = {
    speakerId: string;
    text: string;
    audioIndex: number | null;
};

type ConversationData = {
    speakers: Speaker[];
    lines: ConversationLine[];
};

// ─── Helpers ──────────────────────────────────────────────────────────────────

const SPEECH_LEVELS = [
    { label: "Lost in Translation", threshold: 0,    description: "Your pronunciation is still finding its way—keep practicing!" },
    { label: "Tourist Mode",         threshold: 0.50, description: "You're getting there, but locals might need to guess a bit." },
    { label: "Confident Speaker",    threshold: 0.70, description: "You're understood, and that's a big win!" },
    { label: "Almost Native",        threshold: 0.85, description: "Impressive! Just a few tweaks and you'll fool everyone." },
    { label: "Native-like",          threshold: 0.95, description: "Flawless! Even locals would think you grew up here." },
];

function getLevelForScore(score: number) {
    return (
        [...SPEECH_LEVELS].sort((a, b) => b.threshold - a.threshold).find((l) => score >= l.threshold)
        ?? { label: "Unknown", description: "No feedback available." }
    );
}

function parseConversation(raw: string): ConversationData {
    try { return JSON.parse(raw) as ConversationData; }
    catch { throw new Error("Failed to parse conversation data"); }
}

// ─── Per-user-line state ──────────────────────────────────────────────────────

type UserLineState = {
    audioUrl: string | null;
    resetKey: number;
    isCorrect: boolean;
    isSubmitted: boolean;
    attempts: number;
    level: { label: string; description: string } | null;
};

function makeInitialLineState(): UserLineState {
    return { audioUrl: null, resetKey: 0, isCorrect: false, isSubmitted: false, attempts: 0, level: null };
}

function SpeechLine({ line, audioFiles, isUser, userName }: { line: ConversationLine; audioFiles: string[]; isUser: boolean; userName: string }) {
    if (line.audioIndex === null) {throw new Error("User lines must have an audio index for reference playback"); }
    const audioSrc = `${BASE_URL}${audioFiles[line.audioIndex]}`;
    return (
        <fieldset className={`flex flex-col space-x-2 border rounded-lg p-3 w-fit ${isUser ? 'text-blue-400 border-blue-400' : 'text-gray-400 border-gray-200'}`}>
            <h4 className="font-medium">{userName}</h4>
            <p className='text-sm italic'>{line.text}</p>
            <span>
                {isUser && (
                    <p className="text-xs text-gray-400">Reference:</p>
                )}
                <audio src={audioSrc} controls className="h-8 w-48"/>
            </span>
        </fieldset>
    );
}

// ─── Main Component ───────────────────────────────────────────────────────────

export default function ConversationExercise({ exercise }: { exercise: Exercise }) {
    const audioFiles = exercise.audio_files!;
    const textSupport = exercise.text_support || "";
    const imageFiles = exercise.image_files!;

    const conversation = parseConversation(exercise.question ?? "");

    // State keyed by line index (only user lines have entries)
    const [lineStates, setLineStates] = useState<Record<number, UserLineState>>(() => {
        const conversation = parseConversation(exercise.question ?? "");
        const initial: Record<number, UserLineState> = {};
        conversation.lines.forEach((line, idx) => {
            const speaker = conversation.speakers.find((s) => s.id === line.speakerId);
            if (speaker?.isUser) initial[idx] = makeInitialLineState();
        });
        return initial;
    });
    const [currentLineIndex, setCurrentLineIndex] = useState<number>(() =>
        conversation.lines.findIndex((line) =>
            conversation.speakers.find((s) => s.id === line.speakerId)?.isUser
        )
    );
    const [isLoading, setIsLoading] = useState(false);
    const [isFinished, setIsFinished] = useState(false);

    // Reset when exercise changes
    useEffect(() => {
        if (!conversation) return;
        const initial: Record<number, UserLineState> = {};
        conversation.lines.forEach((line, idx) => {
            const speaker = conversation.speakers.find((s) => s.id === line.speakerId);
            if (speaker?.isUser) initial[idx] = makeInitialLineState();
        });
        setLineStates(initial);
        setCurrentLineIndex(
            conversation.lines.findIndex((line) =>
                conversation.speakers.find((s) => s.id === line.speakerId)?.isUser
            )
        );
    }, [exercise.id]);

    const userLineIndices = conversation.lines.reduce<number[]>((acc, line, idx) => {
        if (conversation.speakers.find((s) => s.id === line.speakerId)?.isUser) acc.push(idx);
        return acc;
    }, []);

    const updateLine = (idx: number, patch: Partial<UserLineState>) =>
        setLineStates((prev) => ({ ...prev, [idx]: { ...prev[idx], ...patch } }));

    const handleEvaluation = async () => {
        const state = lineStates[currentLineIndex];
        if (!state?.audioUrl || isLoading) return;
 
        setIsLoading(true);
 
        try {
            const result = await evaluateSpeech(String(exercise.id), state.audioUrl, conversation.lines[currentLineIndex].audioIndex!);
            const level = getLevelForScore(result.score);
            const newAttempts = state.attempts + 1;
            const isLastUserLine = currentLineIndex === userLineIndices[userLineIndices.length - 1];
 
            if (result.correct) {
                updateLine(currentLineIndex, { isSubmitted: true, isCorrect: true, level });
 
                if (isLastUserLine) {
                    // All lines done — compute allCorrect from previous lines + this one
                    const allCorrect = userLineIndices.every((i) =>
                        i === currentLineIndex ? true : lineStates[i]?.isCorrect
                    );
                    updateScoreById(exercise.id!, allCorrect).catch(console.error);
                    setIsFinished(true);
                } else {
                    const nextUserLine = userLineIndices.find((i) => i > currentLineIndex)!;
                    setCurrentLineIndex(nextUserLine);
                }
            } else {
                updateLine(currentLineIndex, { isSubmitted: true, isCorrect: false, level, attempts: newAttempts });
 
                if (newAttempts >= 3) {
                    updateScoreById(exercise.id!, false).catch(console.error);
                    setIsFinished(true);
                }
            }
        } catch (err) {
            console.error("Error evaluating speaking:", err);
            alert("Failed to evaluate your speech. Please try again.");
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <form className="flex flex-col gap-4">
            <h2>Conversation Exercise</h2>

            {textSupport.trim() !== "" && (
                <section>
                    <h3>Support</h3>
                    <Markdown remarkPlugins={[remarkGfm]}>{textSupport}</Markdown>
                </section>
            )}

            {imageFiles.length > 0 && (
                <section>
                    {imageFiles.map((src, i) => (
                        <Image key={i} src={`${BASE_URL}${src}`} alt="Support" width={300} height={300} />
                    ))}
                </section>
            )}

            <section className="flex flex-col gap-3">
                {conversation.lines.map((line, idx) => {
                    if (idx > currentLineIndex) return;
                    const speaker = conversation.speakers.find((s) => s.id === line.speakerId);
                    if (!speaker) throw new Error(`Speaker with ID ${line.speakerId} not found in conversation data`);
                    if (!lineStates[idx] && speaker.isUser) { throw new Error(`Missing state for line ${idx} - speaker ${line.speakerId}`); }

                    const speakerIdx = conversation.speakers.findIndex((s) => s.id === line.speakerId);
                    const n = conversation.speakers.length;
                    // Each speaker occupies a 1/n-wide column; the column starts at speakerIdx/n of the total width
                    const widthPercent = 100 / n;
                    const marginLeftPercent = (speakerIdx / n) * 100;

                    return (
                        <section
                            className="flex flex-col space-y-4 items-center"
                            key={idx}
                            style={{
                                width: `${widthPercent}%`,
                                marginLeft: `${marginLeftPercent}%`,
                            }}
                        >
                            <SpeechLine
                                line={line}
                                audioFiles={audioFiles}
                                isUser={speaker.isUser}
                                userName={speaker.name}
                            />
                            {speaker.isUser && idx === currentLineIndex && (
                                <span className="flex flex-row space-x-2 items-center">
                                    <AudioRecorder
                                        key={lineStates[idx].resetKey}
                                        onUploadSuccess={(response) => updateLine(idx, { audioUrl: (response as { file_path: string })["file_path"] })}
                                        onUploadError={(err: unknown) => { console.error("Audio upload error:", err); alert("Failed to upload audio. Please try again."); }}
                                    />
                                    <button
                                        type="button"
                                        className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors disabled:cursor-not-allowed disabled:opacity-30"
                                        onClick={() => handleEvaluation()}
                                        disabled={!lineStates[idx].audioUrl|| lineStates[idx].attempts >= 3}
                                    >
                                        {isLoading ? <Ring size={20} color="#fff" /> : "Submit"}
                                    </button>
                                </span>
                            )}
                        </section>
                    );
                })}
            </section>
            {isFinished && (
                <section className={`mt-4 p-3 rounded-lg ${userLineIndices.every((i) => lineStates[i]?.isCorrect) ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
                    <h3 className="text-lg font-semibold">Exercise Completed</h3>
                    <p className="mt-2 text-gray-700">
                        {userLineIndices.every((i) => lineStates[i]?.isCorrect)
                            ? "✓ Correct! Well done!"
                            : `✗ You failed to pronounce some lines correctly (${userLineIndices.filter((i) => lineStates[i]?.isCorrect).length}/${userLineIndices.length} correct)`}
                    </p>
                </section>
            )}
        </form>
    );
}