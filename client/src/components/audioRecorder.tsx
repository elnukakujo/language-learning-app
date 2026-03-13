"use client";

import { useState, useRef, useEffect } from "react";
import { MediaRecorder, register } from "extendable-media-recorder";
import { connect } from "extendable-media-recorder-wav-encoder";
import { uploadAudio } from "@/api";

// ── Register the WAV encoder once (no-op if already registered) ───────────────

let encoderReady: Promise<void> | null = null;

function getEncoderReady(): Promise<void> {
    if (!encoderReady) {
        encoderReady = connect().then(register);
    }
    return encoderReady;
}

// ── Types ─────────────────────────────────────────────────────────────────────

type Status = "idle" | "recording" | "processing" | "uploading" | "done" | "error";

interface AudioRecorderProps {
    onUploadSuccess?: (response: unknown) => void;
    onUploadError?:   (error: unknown)    => void;
}

// ── Component ─────────────────────────────────────────────────────────────────

export default function AudioRecorder({ onUploadSuccess, onUploadError }: AudioRecorderProps) {
    const [status,     setStatus]     = useState<Status>("idle");
    const [previewUrl, setPreviewUrl] = useState<string | null>(null);
    const [errorMsg,   setErrorMsg]   = useState<string>("");

    const previewUrlRef    = useRef<string | null>(null);
    const mediaRecorderRef = useRef<InstanceType<typeof MediaRecorder> | null>(null);
    const chunksRef        = useRef<Blob[]>([]);

    const isRecording  = status === "recording";
    const isProcessing = status === "processing" || status === "uploading";
    const hasRecording = !!previewUrl && (status === "uploading" || status === "done" || status === "error");

    function revokePreview() {
        if (previewUrlRef.current) {
            URL.revokeObjectURL(previewUrlRef.current);
            previewUrlRef.current = null;
        }
    }

    const startRecording = async () => {
        revokePreview();
        setPreviewUrl(null);
        setErrorMsg("");
        chunksRef.current = [];

        // Ensure the WAV encoder worker is registered before recording
        await getEncoderReady();

        const stream = await navigator.mediaDevices.getUserMedia({
            video: false,
            audio: {
                echoCancellation: true,
                noiseSuppression: true,
            },
        });

        // extendable-media-recorder records directly to audio/wav —
        // no manual encoding, no decodeAudioData, no cross-browser hacks needed
        const recorder = new MediaRecorder(stream, { mimeType: "audio/wav" });
        mediaRecorderRef.current = recorder;

        recorder.addEventListener("dataavailable", (e) => {
            if (e.data.size > 0) chunksRef.current.push(e.data);
        });

        recorder.addEventListener("stop", async () => {
            stream.getTracks().forEach((t) => t.stop());
            setStatus("processing");

            try {
                const wavBlob = new Blob(chunksRef.current, { type: "audio/wav" });
                const url     = URL.createObjectURL(wavBlob);
                previewUrlRef.current = url;
                setPreviewUrl(url);

                const file = new File([wavBlob], "recording.wav", { type: "audio/wav" });
                setStatus("uploading");

                uploadAudio(file, true)
                    .then((res) => { setStatus("done");  onUploadSuccess?.(res); })
                    .catch((err) => { setStatus("error"); onUploadError?.(err);  });

            } catch (err) {
                const msg = err instanceof Error ? err.message : String(err);
                console.error("[AudioRecorder] error:", msg);
                setErrorMsg(msg);
                setStatus("error");
            }
        });

        recorder.start(100);
        setStatus("recording");
    };

    const stopRecording = () => mediaRecorderRef.current?.stop();

    useEffect(() => () => revokePreview(), []);

    // ── Render ────────────────────────────────────────────────────────────────

    return (
        <div className="flex flex-col gap-2">
            <div className="flex gap-3 items-center">

                {!isRecording ? (
                    <button
                        type="button"
                        onClick={startRecording}
                        disabled={isProcessing}
                        className="flex items-center gap-2 bg-red-500 text-white px-4 py-2 rounded-lg
                                   hover:bg-red-600 transition-colors disabled:opacity-40 disabled:cursor-not-allowed"
                    >
                        🎙 {hasRecording ? "Re-record" : "Record"}
                    </button>
                ) : (
                    <button
                        type="button"
                        onClick={stopRecording}
                        className="flex items-center gap-2 bg-gray-700 text-white px-4 py-2 rounded-lg
                                   hover:bg-gray-800 transition-colors"
                    >
                        ⏹ Stop
                    </button>
                )}

                {status === "processing" && (
                    <span className="text-sm text-gray-500 animate-pulse">Encoding audio…</span>
                )}
                {status === "uploading" && (
                    <span className="text-sm text-gray-500 animate-pulse">Uploading…</span>
                )}

                {hasRecording && (
                    <audio src={previewUrl!} controls className="h-9" />
                )}
            </div>

            {status === "error" && (
                <span className="text-sm text-red-500">
                    Error: {errorMsg || "Something went wrong — check the console."}
                </span>
            )}
        </div>
    );
}