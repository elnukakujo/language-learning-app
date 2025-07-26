"use client";

import { deleteElement } from "@/api";
import { useRouter } from "next/navigation";
import { useState } from "react";

export default function DeleteButton({ element_id, children }: { element_id: string, children?: React.ReactNode }) {
    const [isDeleting, setIsDeleting] = useState<boolean>(false);

    const elementId = element_id || "";
    const languageId = elementId.split('_')[0].toUpperCase() || "";
    const unitId = elementId.split('_').length > 1 ? languageId + '_' + elementId.split('_')[1]:null;

    const router = useRouter();
    const handleDelete = async () => {
        try {
            await deleteElement(elementId);
            if (elementId.split('_').length>2){
                router.push('/languages/' + languageId + '/unit/' + unitId);
            } else if (elementId.split('_').length===2) {
                router.push('/languages/' + languageId)
            } else {
                router.push('/')
            }
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