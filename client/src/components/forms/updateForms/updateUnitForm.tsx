"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";
import { updateUnit } from "@/api";
import ClassicSelectMenu from "@/components/selectMenu/classicSelectMenu";
import UpdateButton from "@/components/buttons/updateButton";
import type Unit from "@/interface/containers/Unit";
import AutoSizeTextArea from "@/components/textArea/autoSizeTextArea";
import AutoWidthInput from "@/components/input/autoWidthInput";

export default function UpdateUnitForm({ unit }: { unit: Unit }) {
    const router = useRouter();

    const [updatedTitle, setUpdatedTitle] = useState<string | undefined>(unit.title || undefined);
    const [updatedDescription, setUpdatedDescription] = useState<string | undefined>(unit.description || undefined);
    const [updatedLevel, setUpdatedLevel] = useState<'A1' | 'A2' | 'B1' | 'B2' | 'C1' | 'C2'>(unit.level || 'A1');

    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        
        const element: Unit = {
          title: updatedTitle!,
          level: updatedLevel,
          description: updatedDescription || undefined,
          language_id: unit.language_id,
        };
        
        try {
          await updateUnit(unit.id!, element);
          
          const router_path = `/languages/${unit.language_id}`;
          
          router.push(router_path);
          router.refresh();
          
        } catch (error) {
          console.error("Failed to update unit:", error);
          alert("Failed to update unit. Check console for details.");
        }
      };

    return (
        <form className="flex flex-col space-y-4 items-center" onSubmit={handleSubmit}>
            <AutoWidthInput
                value={updatedTitle || ""}
                label="Title"
                onChange={(e) => setUpdatedTitle(e.target.value)}
                placeholder="Enter unit title"
                className="border border-gray-300"
            />

            <AutoSizeTextArea
                value={updatedDescription || ""}
                label="Description"
                onChange={(e) => setUpdatedDescription(e.target.value)}
                placeholder="Enter unit description"
                className="border border-gray-300"
            />

            <ClassicSelectMenu
                label="Level"
                options={['A1', 'A2', 'B1', 'B2', 'C1', 'C2']}
                selectedOption={updatedLevel}
                onChange={(value) => setUpdatedLevel(value as typeof updatedLevel)}
                required={true}
            />
            
            <UpdateButton>Update Unit</UpdateButton>
        </form>
    );
}