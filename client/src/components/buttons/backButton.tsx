"use client";

import { useRouter } from "next/navigation";

export default function BackButton({ children }: { children?: React.ReactNode }) {
    const router = useRouter();
    const handleClick = () => {
        const pathname = window.location.pathname;
        let parentPath = pathname.substring(0, pathname.lastIndexOf('/')) || '/';
        while (/(voc|gram|char|unit|languages)$/.test(parentPath)) {
            parentPath = parentPath.substring(0, parentPath.lastIndexOf('/')) || '/';
        }
        router.push(parentPath);
    };

    return (
        <button
        className="border-2 rounded px-4 py-2"
        onClick={handleClick}
        >
            <i className="bi bi-arrow-left">{children || "Back"}</i>
        </button>
    );
}