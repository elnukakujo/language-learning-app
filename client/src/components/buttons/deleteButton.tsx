"use client";

import { deleteElement } from "@/api";
import { useRouter } from "next/navigation";
import { useState } from "react";

export default function DeleteButton({ element_id, children }: { element_id: string, children?: React.ReactNode }) {
    const [isDeleting, setIsDeleting] = useState<boolean>(false);

    const router = useRouter();
    const handleDelete = async () => {
        try {
            await deleteElement(element_id);
            const pathname = window.location.pathname;
            let parentPath = pathname.substring(0, pathname.lastIndexOf('/')) || '/';
            while (/(voc|gram|call|unit|languages)$/.test(parentPath)) {
                parentPath = parentPath.substring(0, parentPath.lastIndexOf('/')) || '/';
            }
            router.push(parentPath);
            // Optionally, you can add some success feedback here
        } catch (error) {
        console.error("Failed to delete element:", error);
        // Optionally, you can add some error feedback here
        }
    };

    return (
        <div>
            <button type="button" onClick={() => setIsDeleting(true)} className="border-2 rounded px-4 py-2">
                {children || "Delete Element"}
            </button>
            {isDeleting && (
                <span>
                    <p>Are you sure you want to delete this element?</p>
                    <button type="button" onClick={handleDelete} className="border-2 rounded px-4 py-2">
                        Confirm Delete
                    </button>
                    <button type="button" onClick={() => setIsDeleting(false)} className="border-2 rounded px-4 py-2">
                        Cancel
                    </button>
                </span>
            )}
        </div>
    );
}