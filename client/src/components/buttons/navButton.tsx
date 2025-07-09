"use client";   

import { useRouter } from "next/navigation";

export default function NavButton({ children, path }: { children?: React.ReactNode, path: string }) {
    const router = useRouter();

    return (
        <button className='border-2 rounded px-4 py-2' onClick={() => router.push(path)}>
            {children}
        </button>
    );
}