"use client";

import { useState } from "react";
import UpdateButton from "@/components/buttons/updateButton";
import type Unit from "@/interface/Unit";
import AutoSizeTextArea from "@/components/textArea/autoSizeTextArea";
import AutoWidthInput from "@/components/input/autoWidthInput";

export default function UpdateUnitForm({ unit }: { unit: Unit }) {
    const [updatedTitle, setUpdatedTitle] = useState<string>(unit.title);
    const [updatedDescription, setUpdatedDescription] = useState<string>(unit.description||"");

    return (
        <form className="flex flex-col space-y-4 items-center">
            <AutoWidthInput
                value={updatedTitle}
                label="Title"
                onChange={(e) => setUpdatedTitle(e.target.value)}
                placeholder="Enter unit title"
                className="border border-gray-300"
            />

            <AutoSizeTextArea
                value={updatedDescription}
                label="Description"
                onChange={(e) => setUpdatedDescription(e.target.value)}
                placeholder="Enter unit description"
                className="border border-gray-300"
            />
            
            <UpdateButton
                element={{
                    type_element: "unit",
                    id: unit.id,
                    title: updatedTitle,
                    description: updatedDescription,
                    language_id: unit.language_id,
                }}
            />
        </form>
    );
}