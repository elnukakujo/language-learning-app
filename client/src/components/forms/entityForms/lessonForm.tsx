"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import NewElementButton from "@/components/buttons/newElementButton";
import UpdateButton from "@/components/buttons/updateButton";
import AutoWidthInput from "@/components/input/autoWidthInput";
import AutoSizeTextArea from "@/components/textArea/autoSizeTextArea";
import ClassicSelectMenu from "@/components/selectMenu/classicSelectMenu";
import TagSelector from "@/components/selectMenu/tagSelector";
import { createLesson, updateLesson } from "@/api/lesson";
import type Lesson from "@/interface/containers/Lesson";
import SourceSelector from "@/components/selectMenu/sourceSelector";

const LEVEL_OPTIONS: Array<Lesson["level"]> = ["A1", "A2", "B1", "B2", "C1", "C2"];

export default function LessonForm({ lesson, language_id }: { lesson?: Partial<Lesson>; language_id: string }) {
    const router = useRouter();
    const isUpdate = Boolean(lesson?.id);
    let lessonData: Partial<Lesson>;
    if (!lesson) {
        lessonData = {
            language_id: language_id,
            title: "",
            description: "",
            level: "A1"
        };
    } else {
        lessonData = lesson;
    }

    const [title, setTitle] = useState<string>(lessonData.title || "");
    const [description, setDescription] = useState<string | undefined>(lessonData.description);
    const [level, setLevel] = useState<Lesson["level"]>(lessonData.level || "A1");
    const [selectedTagIds, setSelectedTagIds] = useState<string[]>(lessonData.tags ? lessonData.tags.map(tag => tag.id!) : []);
    const [selectedSourceIds, setSelectedSourceIds] = useState<string[]>(lessonData.sources ? lessonData.sources.map(source => source.id!) : []);

    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();

        const element: Partial<Lesson> = {
            title: title,
            level: level,
            description: description,
            language_id: language_id,
            tags: selectedTagIds.map(id => ({ id })),
            sources: selectedSourceIds.map(id => ({ id }))
        };

        try {
            let lessonId: string;
            if (isUpdate) {
                await updateLesson(lessonData.id!, element);
                lessonId = lessonData.id!;
            } else {
                const response = await createLesson(element);
                lessonId = response.id;
            }

            router.push(`/languages/${language_id}`);
            router.refresh();
        } catch (error) {
            console.error(`Failed to ${isUpdate ? "update" : "create"} lesson:`, error);
            alert(`Failed to ${isUpdate ? "update" : "create"} lesson. Check console for details.`);
        }
    };

    return (
        <form className="flex flex-col space-y-4 items-center" onSubmit={handleSubmit}>
            <AutoWidthInput
                value={title}
                label="Title"
                onChange={(e) => setTitle(e.target.value)}
                placeholder="Enter lesson title"
                className="border border-gray-300"
                required={true}
            />

            <AutoSizeTextArea
                value={description || ""}
                label="Description"
                onChange={(e) => setDescription(e.target.value)}
                placeholder="Enter lesson description"
                className="border border-gray-300"
            />

            <ClassicSelectMenu
                label="Level"
                options={LEVEL_OPTIONS}
                selectedOption={level}
                onChange={(value) => setLevel(value as Lesson["level"])}
                required={true}
            />

            <TagSelector
                selectedTagIds={selectedTagIds}
                onTagsChange={setSelectedTagIds}
                elementId={lessonData.id!}
            />
            <SourceSelector
                selectedSourceIds={selectedSourceIds}
                onSourcesChange={setSelectedSourceIds}
                elementId={lessonData.id!}
            />

            {isUpdate ? <UpdateButton>Update Lesson</UpdateButton> : <NewElementButton>Add Lesson</NewElementButton>}
        </form>
    );
}