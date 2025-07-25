"use client";

import { deleteElement } from "@/api";
import { useRouter } from "next/navigation";

export default function DeleteButton({ element_id, children }: { element_id: string, children?: React.ReactNode }) {
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
        <button type="button" onClick={handleDelete} className="border-2 rounded px-4 py-2">
            {children || "Delete Element"}
        </button>
    );
}