"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import UpdateButton from "@/components/buttons/updateButton";
import AutoSizeTextArea from "@/components/textArea/autoSizeTextArea";
import AutoWidthInput from "@/components/input/autoWidthInput";
import type Language from "@/interface/containers/Language";
import { updateLanguage } from "@/api";
import ClassicSelectMenu from "@/components/selectMenu/classicSelectMenu";

export default function UpdateLanguageForm({ language }: { language: Language }) {
    const router = useRouter();

    const [updatedName, setUpdatedName] = useState<string | undefined>(language.name || undefined);
    const [updatedNativeName, setUpdatedNativeName] = useState<string | undefined>(language.native_name || undefined);
    const [updatedDescription, setUpdatedDescription] = useState<string | undefined>(language.description || undefined);
    const [updatedLevel, setUpdatedLevel] = useState<'A1' | 'A2' | 'B1' | 'B2' | 'C1' | 'C2'>(language.level || "A1");
    const [updatedFlag, setUpdatedFlag] = useState<string | undefined>(language.flag || undefined);

    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        
        const element: Language = {
          name: updatedName!,
          native_name: updatedNativeName!,
          description: updatedDescription || undefined,
          level: updatedLevel,
          flag: updatedFlag || undefined
        };
        
        try {
          await updateLanguage(language.id!, element);
          
          router.push('/');
          router.refresh();
          
        } catch (error) {
          console.error("Failed to update language:", error);
          alert("Failed to update language. Check console for details.");
        }
      };

    return (
        <form className="flex flex-col space-y-4 items-center" onSubmit={handleSubmit}>
            <AutoWidthInput
                value={updatedName || ""}
                label="Name"
                onChange={(e) => setUpdatedName(e.target.value)}
                placeholder="Enter language name"
                className="border border-gray-300"
            />
            <AutoWidthInput
                value={updatedNativeName || ""}
                label="Native Name"
                onChange={(e) => setUpdatedNativeName(e.target.value)}
                placeholder="Enter native name"
                className="border border-gray-300"
            />
            <AutoSizeTextArea
                value={updatedDescription || ""}
                label="Description"
                onChange={(e) => setUpdatedDescription(e.target.value)}
                placeholder="Enter description"
                className="border border-gray-300"
            />
            <ClassicSelectMenu
                label="Level"
                options={['A1', 'A2', 'B1', 'B2', 'C1', 'C2']}
                selectedOption={updatedLevel}
                onChange={(value) => setUpdatedLevel(value as typeof updatedLevel)}
                required={true}
            />
            <AutoWidthInput
                value={updatedFlag || ""}
                label="Flag"
                onChange={(e) => setUpdatedFlag(e.target.value)}
                placeholder="Enter flag"
                className="border border-gray-300"
            />
            
            <UpdateButton>Update Language</UpdateButton>
        </form>
    );
}