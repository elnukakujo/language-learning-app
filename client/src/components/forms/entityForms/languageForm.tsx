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

const LANGUAGE_to_ISO639_2T: Record<string, string> = {
    "Catalan": "cat",
    "Chinois": "zho",
    "Croatian": "hrv",
    "Danish": "dan",
    "Dutch": "nld",
    "English": "eng",
    "Finnish": "fin",
    "French": "fra",
    "German": "deu",
    "Greek": "ell",
    "Italian": "ita",
    "Japanese": "jpn",
    "Korean": "kor",
    "Lithuanian": "lit",
    "Macedonian": "mkd",
    "Norwegian Bokmål": "nob",
    "Norwegian": "nor",
    "Polish": "pol",
    "Portuguese": "por",
    "Romanian": "ron",
    "Russian": "rus",
    "Slovenian": "slv",
    "Spanish": "spa",
    "Swedish": "swe",
    "Ukrainian": "ukr",
    "Not Specified": "",
    // Add more languages as needed
};

const ISO639_2T_to_LANGUAGE: Record<string, string> = Object.fromEntries(
    Object.entries(LANGUAGE_to_ISO639_2T).map(([language, iso]) => [iso, language])
);

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
            target_iso639_2t: "",
            source_iso639_2t: "",
        };
    } else {
        languageData = language;
    }

    const [name, setName] = useState<string>(languageData.name);
    const [nativeName, setNativeName] = useState<string | undefined>(languageData.native_name);
    const [description, setDescription] = useState<string | undefined>(languageData.description);
    const [level, setLevel] = useState<Language["level"]>(languageData.level);
    const [flag, setFlag] = useState<string | undefined>(languageData.flag);
    const [targetIso639_2t, setTargetIso639_2t] = useState<string | undefined>(languageData.target_iso639_2t);
    const [sourceIso639_2t, setSourceIso639_2t] = useState<string | undefined>(languageData.source_iso639_2t);

    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();

        const element: Language = {
            name,
            native_name: nativeName || undefined,
            description: description || undefined,
            level,
            flag: flag || undefined,
            target_iso639_2t: targetIso639_2t || undefined,
            source_iso639_2t: sourceIso639_2t || undefined,
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
                onChange={(e) => {
                    setName(e.target.value);
                    setTargetIso639_2t(LANGUAGE_to_ISO639_2T[e.target.value] || "");
                }}
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

            <ClassicSelectMenu
                label="Language Used to Study"
                options={Object.keys(LANGUAGE_to_ISO639_2T)}
                selectedOption={ISO639_2T_to_LANGUAGE[sourceIso639_2t || ""] || ""}
                onChange={(value) => setSourceIso639_2t(LANGUAGE_to_ISO639_2T[value] || "")}
                required
            />

            {isUpdate ? <UpdateButton>Update Language</UpdateButton> : <NewElementButton>Add Language</NewElementButton>}
        </form>
    );
}