"use client";   

import { useRouter } from "next/navigation";

export default function NavButton({ children, path, className }: { children?: React.ReactNode, path: string, className?: string }) {
    const router = useRouter();

    return (
        <button className={className || 'btn btn-secondary'} onClick={() => router.push(path)}>
            {children}
        </button>
    );
}