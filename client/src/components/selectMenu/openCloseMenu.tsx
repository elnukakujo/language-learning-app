"use client";

import { useState } from "react";

type Element = {
    id: string;
    value: string;
};

export default function OpenCloseMenu({ 
    elements, 
    selectedElements,
    setSelectedElements,
    label
} : { 
    elements: Element[], 
    selectedElements: string[],
    setSelectedElements: (elements: string[]) => void,
    label?: string
}) {

    const [isOpen, setIsOpen] = useState(false);

    return (
        <menu>
            {label && <label className="block text-sm font-medium text-gray-700">
                {label}
            </label>}
            <button
                type="button"
                onClick={() => setIsOpen(!isOpen)}
                className="text-blue-600 button"
            >
                {isOpen ? "Hide" : "Show"}
            </button>
            {isOpen && (
                <ul className="max-w-[40rem] flex flex-row flex-wrap gap-2 mt-2">
                    {elements.map((item) => (
                        <li key={item.id}>
                        <button
                            type="button"
                            onClick={() => {
                            setSelectedElements(
                                selectedElements.includes(item.id) ? 
                                selectedElements.filter(id => id !== item.id) : 
                                [...selectedElements, item.id]
                            );
                            }}
                            className={`px-2 py-1 rounded-md ${
                            selectedElements.includes(item.id) ? "bg-blue-600" : "bg-gray-700"
                            }`}
                        >
                            {item.value}
                        </button>
                        
                        </li>
                    ))}
                </ul>
            )}
        </menu>
    );
}