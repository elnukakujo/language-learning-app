"use client";

import { useState } from "react";
import UpdateButton from "@/components/buttons/updateButton";
import AutoSizeTextArea from "@/components/textArea/autoSizeTextArea";
import AutoWidthInput from "@/components/input/autoWidthInput";
import type Language from "@/interface/Language";

export default function UpdateLanguageForm({ language }: { language: Language }) {
    const [updatedName, setUpdatedName] = useState<string>(language.name);
    const [updatedNativeName, setUpdatedNativeName] = useState<string>(language.native_name || "");
    const [updatedFlag, setUpdatedFlag] = useState<string>(language.flag || "");
    const [updatedLevel, setUpdatedLevel] = useState<string>(language.level || "A1");
    const [updatedDescription, setUpdatedDescription] = useState<string>(language.description||"");

    return (
        <form className="flex flex-col space-y-4 items-center">
            <AutoWidthInput
                value={updatedName}
                label="Name"
                onChange={(e) => setUpdatedName(e.target.value)}
                placeholder="Enter language name"
                className="border border-gray-300"
            />
            <AutoWidthInput
                value={updatedNativeName}
                label="Native Name"
                onChange={(e) => setUpdatedNativeName(e.target.value)}
                placeholder="Enter native name"
                className="border border-gray-300"
            />
            <AutoWidthInput
                value={updatedFlag}
                label="Flag"
                onChange={(e) => setUpdatedFlag(e.target.value)}
                placeholder="Enter flag"
                className="border border-gray-300"
            />
            <AutoWidthInput
                value={updatedLevel}
                label="Level"
                onChange={(e) => setUpdatedLevel(e.target.value)}
                placeholder="Enter level"
                className="border border-gray-300"
            />

            <AutoSizeTextArea
                value={updatedDescription}
                label="Description"
                onChange={(e) => setUpdatedDescription(e.target.value)}
                placeholder="Enter description"
                className="border border-gray-300"
            />
            
            <UpdateButton
                element={{
                    type_element: "lang",
                    id: language.id,
                    name: updatedName,
                    native_name: updatedNativeName,
                    flag: updatedFlag,
                    level: updatedLevel,
                    description: updatedDescription
                }}
            />
        </form>
    );
}