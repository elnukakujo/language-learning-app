"use client";
import { useState, useRef, useEffect } from "react";
import { useRouter } from "next/navigation";
import Source from '@/interface/systemData/Source';
import { createSource, updateSource } from "@/api";
import AutoWidthInput from "@/components/input/autoWidthInput";
import AutoSizeTextArea from "@/components/textArea/autoSizeTextArea";
import UpdateButton from "@/components/buttons/updateButton";
import NewElementButton from "@/components/buttons/newElementButton";
import ClassicSelectMenu from "@/components/selectMenu/classicSelectMenu";

export default function SourceForm({ source, navDisabled = false, onSuccess }: { source?: Source | Partial<Source>, navDisabled?: boolean, onSuccess?: () => void }) {
    const isUpdate = Boolean(source?.id);
    const router = useRouter();

    const sourceData: Partial<Source> = source ?? {
        id: "", user_id: "user_U0", title: "", date: "", description: "", source_type: ""
    };

    const [title, setTitle] = useState<string>(sourceData.title || "");
    const [description, setDescription] = useState<string>(sourceData.description || "");
    const [sourceType, setSourceType] = useState<string>(sourceData.source_type || "original");

    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        const element: Partial<Source> = {
            id: sourceData.id,
            user_id: sourceData.user_id || "user_U0",
            title,
            source_type: sourceType,
            description,
        };
        try {
        if (isUpdate) {
            await updateSource(sourceData.id!, element);
        } else {
            await createSource(element);
        }
        if (!navDisabled) {
            router.push(`/sources`);
            router.refresh();
        }
        } catch (error) {
        console.error("Error creating/updating source:", error);
        alert(`Failed to ${isUpdate ? "update" : "create"} source.`);
        } finally {
        if (onSuccess) onSuccess();
        }
    };

    return (
        <form onSubmit={handleSubmit} className="flex flex-col gap-4 items-center">
        <AutoWidthInput
            label="Name"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="Source name"
            required
        />

        <ClassicSelectMenu
            label="Source Type"
            options={[ "original", "textbook", "class", "online", "media", "social", "other" ]}
            selectedOption={sourceType}
            onChange={(e) => setSourceType(e)}
            required
        />

        <AutoSizeTextArea
            label="Description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
        />

        {isUpdate ? <UpdateButton>Update Source</UpdateButton> : <NewElementButton>Add Source</NewElementButton>}
        </form>
    );
}