"use client";

import { useRouter } from "next/navigation";

export default function BackButton({ children }: { children?: React.ReactNode }) {
    const router = useRouter();

    return (
        <button
        className="border-2 rounded px-4 py-2"
        onClick={() => router.back()}
        >
            <i className="bi bi-arrow-left">{children || "Back"}</i>
        </button>
    );
}