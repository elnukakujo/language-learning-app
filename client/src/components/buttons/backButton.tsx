"use client";

import { useRouter } from "next/navigation";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import { faArrowLeft } from "@fortawesome/free-solid-svg-icons";

export default function BackButton({ children }: { children?: React.ReactNode }) {
    const router = useRouter();
    const handleClick = () => {
        const pathname = window.location.pathname;
        let parentPath = pathname.substring(0, pathname.lastIndexOf('/')) || '/';
        while (/(voc|gram|call|lesson|languages|new|ex|sources|tags|passage|character|word)$/.test(parentPath)) {
            parentPath = parentPath.substring(0, parentPath.lastIndexOf('/')) || '/';
        }
        router.push(parentPath);
    };

    return (
        <button
        className="border-2 rounded px-4 py-2 border-gray-300 hover:bg-gray-100"
        onClick={handleClick}
        >
            <FontAwesomeIcon icon={faArrowLeft} className="text-gray-500 hover:text-gray-700" />
            {children}
        </button>
    );
}