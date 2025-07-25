"use client";

import { useState, useRef, useEffect } from "react";
import NewElementButton from "@/components/buttons/newElementButton";

export default function CreateLanguageForm() {
    const [name, setName] = useState<string>("");
    const [nativeName, setNativeName] = useState<string>("");
    const [flag, setFlag] = useState<string>("");
    const [level, setLevel] = useState<string>("");
    const [description, setDescription] = useState<string>("");

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
                {[name, nativeName, flag, level].map((field, index) => (
                    <span key={index} className="flex flex-col space-y-2 h-fit">
                        <label htmlFor={`field-${index}`} key={index}>
                            {["Name*", "Native Name", "Flag", "Level"][index]}
                        </label>
                        <input
                            key={'char'+index}
                            type="text"
                            value={field}
                            onChange={(e) => {
                                const newValue = e.target.value;
                                if (index === 0) setName(newValue);
                                if (index === 1) setNativeName(newValue);
                                if (index === 2) setFlag(newValue);
                                if (index === 3) setLevel(newValue);
                            }}
                            className="border border-gray-300 rounded p-2 w-full"
                        />
                    </span>   
                ))}
                <span className="flex flex-col space-y-2 h-fit">
                    <label htmlFor="description">Description</label>
                    <textarea 
                        ref={descriptionRef}
                        name="description" 
                        id="description" 
                        value={description} 
                        onChange={(e) => setDescription(e.target.value)}
                        className="border border-gray-300 rounded-md p-2 h-fit"
                    />
                </span>
            </div>
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