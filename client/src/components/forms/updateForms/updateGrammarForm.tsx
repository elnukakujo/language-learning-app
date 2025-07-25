"use client";

import { useState, useRef, useEffect } from "react";
import UpdateButton from "@/components/buttons/updateButton";
import ChangeUnitMenu from "@/components/selectMenu/changeUnitMenu";
import type Grammar from "@/interface/Grammar";

export default function updateGrammarForm({ grammar, existingUnitsId }: { grammar: Grammar, existingUnitsId: string[] }) {
  const [updatedTitle, setUpdatedTitle] = useState<string>(grammar.title);
  const [updatedExplanation, setUpdatedExplanation] = useState<string>(grammar.explanation);

  const [unitId, setUnitId] = useState<string>(grammar.unit_id);

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
        <ChangeUnitMenu unitsId={existingUnitsId} unitId={unitId} onChange={setUnitId} />
        <label htmlFor="title">Title</label>
        <input
          type="text"
          id="title"
          name="title"
          value={updatedTitle}
          onChange={(e) => setUpdatedTitle(e.target.value)}
          className="border border-gray-300 rounded-md p-2 h-fit"
        />
      </div>

      <div className="flex flex-col space-y-2 h-fit">
        <label htmlFor="explanation">Explanation</label>
        <textarea
          ref={textareaRef}
          id="explanation"
          name="explanation"
          value={updatedExplanation}
          onChange={(e) => {
            setUpdatedExplanation(e.target.value);
            e.target.style.height = "auto";
            e.target.style.height = `${e.target.scrollHeight}px`;
          }}
          className="flex resize-none overflow-hidden border border-gray-300 rounded-md p-2"
        />
      </div>

      <UpdateButton
        element={{
          type_element: "gram",
          id: grammar.id,
          title: updatedTitle,
          explanation: updatedExplanation,
          score: grammar.score,
          last_seen: grammar.last_seen,
          unit_id: unitId,
        }}
      />
    </form>
  );
}
