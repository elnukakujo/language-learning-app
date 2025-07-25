"use client";

import { useState, useRef, useEffect } from "react";
import UpdateButton from "@/components/buttons/updateButton";
import type Unit from "@/interface/Unit";

export default function UpdateUnitForm({ unit }: { unit: Unit }) {
    const [title, setTitle] = useState<string>(unit.title);
    const [description, setDescription] = useState<string>(unit.description||"");

    const descriptionRef = useRef<HTMLTextAreaElement>(null);
    useEffect(() => {
        if (descriptionRef.current) {
            descriptionRef.current.style.height = "auto";
            descriptionRef.current.style.height = `${descriptionRef.current.scrollHeight}px`;
        }
    }, [description]);

    return (
        <form className="flex flex-col space-y-4">
            <div className="flex flex-col space-y-2 h-fit">
                <label htmlFor="title">Title</label>
                <input type="text" value={title} onChange={(e) => setTitle(e.target.value)} className="border border-gray-300 rounded-md p-2 h-fit"/>
                <label htmlFor="description">Description</label>
                <textarea 
                    ref={descriptionRef}
                    name="description" 
                    id="description" 
                    value={description} 
                    onChange={(e) => setDescription(e.target.value)}
                    className="border border-gray-300 rounded-md p-2 h-fit"
                />
            </div>
            <UpdateButton
                element={{
                    type_element: "unit",
                    id: unit.id,
                    title: title,
                    description: description,
                    language_id: unit.language_id,
                }}
            />
        </form>
    );
}