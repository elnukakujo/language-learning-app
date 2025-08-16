"use client";

import { useState } from "react";
import NewElementButton from "@/components/buttons/newElementButton";
import AutoWidthInput from "@/components/input/autoWidthInput";
import AutoSizeTextArea from "@/components/textArea/autoSizeTextArea";

export default function CreateLanguageForm() {
    const [name, setName] = useState<string>("");
    const [nativeName, setNativeName] = useState<string>("");
    const [flag, setFlag] = useState<string>("");
    const [level, setLevel] = useState<string>("");
    const [description, setDescription] = useState<string>("");

    return (
        <form className="flex flex-col space-y-4 items-center">
            <AutoWidthInput
                value={name}
                label="Name"
                onChange={(e) => setName(e.target.value)}
                placeholder="Enter language name"
                className="border border-gray-300"
            />
            <AutoWidthInput
                value={nativeName}
                label="Native Name"
                onChange={(e) => setNativeName(e.target.value)}
                placeholder="Enter native name"
                className="border border-gray-300"
            />
            <AutoWidthInput
                value={flag}
                label="Flag"
                onChange={(e) => setFlag(e.target.value)}
                placeholder="Enter flag"
                className="border border-gray-300"
            />
            <AutoWidthInput
                value={level}
                label="Level"
                onChange={(e) => setLevel(e.target.value)}
                placeholder="Enter level"
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
                    type_element: "lang",
                    id: "",
                    name: name,
                    native_name: nativeName,
                    flag: flag,
                    level: level,
                    description: description
                }}
            />
        </form>
    );
}