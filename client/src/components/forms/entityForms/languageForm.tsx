"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import NewElementButton from "@/components/buttons/newElementButton";
import UpdateButton from "@/components/buttons/updateButton";
import AutoWidthInput from "@/components/input/autoWidthInput";
import AutoSizeTextArea from "@/components/textArea/autoSizeTextArea";
import ClassicSelectMenu from "@/components/selectMenu/classicSelectMenu";
import { createLanguage, updateLanguage } from "@/api";
import type Language from "@/interface/containers/Language";

const LEVEL_OPTIONS: Array<Language["level"]> = ["A1", "A2", "B1", "B2", "C1", "C2"];

export default function LanguageForm({language}: { language?: Language }) {
    const router = useRouter();
    const isUpdate = Boolean(language);
    let languageData: Language;
    if (!language) {
        languageData = {
            name: "",
            native_name: "",
            description: "",
            level: "A1",
            flag: "",
        };
    } else {
        languageData = language;
    }

    const [name, setName] = useState<string>(languageData.name);
    const [nativeName, setNativeName] = useState<string | undefined>(languageData.native_name);
    const [description, setDescription] = useState<string | undefined>(languageData.description);
    const [level, setLevel] = useState<Language["level"]>(languageData.level);
    const [flag, setFlag] = useState<string | undefined>(languageData.flag);

    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();

        const element: Language = {
            name,
            native_name: nativeName || undefined,
            description: description || undefined,
            level,
            flag: flag || undefined,
        };

        try {
            if (isUpdate) {
                await updateLanguage(languageData.id!, element);
            } else {
                await createLanguage(element);
            }

            router.push("/");
            router.refresh();
        } catch (error) {
            console.error(`Failed to ${isUpdate ? "update" : "create"} language:`, error);
            alert(`Failed to ${isUpdate ? "update" : "create"} language. Check console for details.`);
        }
    };

    return (
        <form className="flex flex-col space-y-4 items-center" onSubmit={handleSubmit}>
            <AutoWidthInput
                value={name}
                label="Name"
                onChange={(e) => setName(e.target.value)}
                placeholder="Enter language name"
                className="border border-gray-300"
                required
            />

            <AutoWidthInput
                value={nativeName || ""}
                label="Native Name"
                onChange={(e) => setNativeName(e.target.value)}
                placeholder="Enter native name"
                className="border border-gray-300"
            />

            <AutoSizeTextArea
                value={description || ""}
                onChange={(e) => setDescription(e.target.value)}
                className="border border-gray-300"
                label="Description"
                placeholder="Enter description"
            />

            <ClassicSelectMenu
                label="Level"
                options={LEVEL_OPTIONS}
                selectedOption={level}
                onChange={(value) => setLevel(value as Language["level"])}
                required
            />

            <AutoWidthInput
                value={flag || ""}
                label="Flag"
                onChange={(e) => setFlag(e.target.value)}
                placeholder="Enter flag"
                className="border border-gray-300"
            />

            {isUpdate ? <UpdateButton>Update Language</UpdateButton> : <NewElementButton>Add Language</NewElementButton>}
        </form>
    );
}