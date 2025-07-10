"use client";

import { useState, useRef, useEffect} from "react";

import NewElementButton from "@/components/buttons/newElementButton";

export default function createGrammarForm({unit_id}: {unit_id: string}) {
    const [title, setTitle] = useState("");
    const [explanation, setExplanation] = useState("");

    const textareaRef = useRef<HTMLTextAreaElement>(null);
  
    useEffect(() => {
      const textarea = textareaRef.current;
      if (textarea) {
        textarea.style.height = "auto";
        textarea.style.height = `${textarea.scrollHeight}px`;
      }
    }, []);
  
    return (
      <form className="flex flex-col space-y-4">
        <div className="flex flex-col space-y-2 h-fit">
          <label htmlFor="title">Title*</label>
          <input
            type="text"
            id="title"
            name="title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            className="border border-gray-300 rounded-md p-2 h-fit"
          />
        </div>
  
        <div className="flex flex-col space-y-2 h-fit">
          <label htmlFor="explanation">Explanation*</label>
          <textarea
            ref={textareaRef}
            id="explanation"
            name="explanation"
            value={explanation}
            onChange={(e) => {
              setExplanation(e.target.value);
              e.target.style.height = "auto";
              e.target.style.height = `${e.target.scrollHeight}px`;
            }}
            className="flex resize-none overflow-hidden border border-gray-300 rounded-md p-2"
          />
        </div>

      <NewElementButton
        element={{
          type_element: "gram",
          id: "",
          title: title,
          explanation: explanation,
          score: 0,
          last_seen: new Date(),
          unit_id: unit_id
        }}
      />
    </form>
  );
}
