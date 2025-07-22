"use client";

import { deleteElement } from "@/api";
import { useRouter } from "next/navigation";

export default function DeleteButton({ element_id, children }: { element_id: string, children?: React.ReactNode }) {
    const languageId = element_id.split('_')[0].toUpperCase();
    const unitId = languageId + '_' + element_id.split('_')[1];

    const router = useRouter();
    const handleDelete = async () => {
        try {
            await deleteElement(element_id);
            router.push('/languages/' + languageId + '/unit/' + unitId);
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