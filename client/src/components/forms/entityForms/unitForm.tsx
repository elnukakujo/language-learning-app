"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import NewElementButton from "@/components/buttons/newElementButton";
import UpdateButton from "@/components/buttons/updateButton";
import AutoWidthInput from "@/components/input/autoWidthInput";
import AutoSizeTextArea from "@/components/textArea/autoSizeTextArea";
import ClassicSelectMenu from "@/components/selectMenu/classicSelectMenu";
import { createUnit, updateUnit } from "@/api";
import type Unit from "@/interface/containers/Unit";

const LEVEL_OPTIONS: Array<Unit["level"]> = ["A1", "A2", "B1", "B2", "C1", "C2"];

export default function UnitForm({ unit, language_id }: { unit?: Unit; language_id: string }) {
    const router = useRouter();
    const isUpdate = Boolean(unit);
    let unitData: Unit;
    if (!unit) {
        unitData = {
            language_id: language_id,
            title: "",
            description: "",
            level: "A1"
        };
    } else {
        unitData = unit;
    }

    const [title, setTitle] = useState<string>(unitData.title);
    const [description, setDescription] = useState<string | undefined>(unitData.description);
    const [level, setLevel] = useState<Unit["level"]>(unitData.level);

    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();

        const element: Unit = {
            title: title,
            level: level,
            description: description,
            language_id: language_id,
        };

        try {
            if (isUpdate) {
                await updateUnit(unitData.id!, element);
            } else {
                await createUnit(element);
            }

            router.push(`/languages/${language_id}`);
            router.refresh();
        } catch (error) {
            console.error(`Failed to ${isUpdate ? "update" : "create"} unit:`, error);
            alert(`Failed to ${isUpdate ? "update" : "create"} unit. Check console for details.`);
        }
    };

    return (
        <form className="flex flex-col space-y-4 items-center" onSubmit={handleSubmit}>
            <AutoWidthInput
                value={title}
                label="Title"
                onChange={(e) => setTitle(e.target.value)}
                placeholder="Enter unit title"
                className="border border-gray-300"
                required={true}
            />

            <AutoSizeTextArea
                value={description || ""}
                label="Description"
                onChange={(e) => setDescription(e.target.value)}
                placeholder="Enter unit description"
                className="border border-gray-300"
            />

            <ClassicSelectMenu
                label="Level"
                options={LEVEL_OPTIONS}
                selectedOption={level}
                onChange={(value) => setLevel(value as Unit["level"])}
                required={true}
            />

            {isUpdate ? <UpdateButton>Update Unit</UpdateButton> : <NewElementButton>Add Unit</NewElementButton>}
        </form>
    );
}