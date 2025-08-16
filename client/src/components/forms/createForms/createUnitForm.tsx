"use client";

import { useState } from "react";
import NewElementButton from "@/components/buttons/newElementButton";
import AutoWidthInput from "@/components/input/autoWidthInput";
import AutoSizeTextArea from "@/components/textArea/autoSizeTextArea";

export default function CreateUnitForm({ language_id }: { language_id: string }) {
    const [title, setTitle] = useState<string>("");
    const [description, setDescription] = useState<string>("");

    return (
        <form className="flex flex-col space-y-4 items-center">
            <AutoWidthInput
                value={title}
                label="Title"
                onChange={(e) => setTitle(e.target.value)}
                placeholder="Enter unit title"
                className="border border-gray-300"
            />
            <AutoSizeTextArea
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                className="border border-gray-300"
                label="Description"
            />
            <NewElementButton
                element={{
                    type_element: "unit",
                    id: "",
                    title: title,
                    description: description,
                    language_id: language_id,
                }}
            />
        </form>
    );
}