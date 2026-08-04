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
        className="btn btn-secondary"
        onClick={handleClick}
        >
            <FontAwesomeIcon icon={faArrowLeft} />
            {children}
        </button>
    );
}