"use client";

import { useState } from "react";
import UpdateButton from "@/components/buttons/updateButton";
import ChangeUnitMenu from "@/components/selectMenu/changeUnitMenu";
import type Grammar from "@/interface/features/Grammar";
import AutoWidthInput from "@/components/input/autoWidthInput";
import AutoSizeTextArea from "@/components/textArea/autoSizeTextArea";

export default function updateGrammarForm({ grammar, existingUnitsId }: { grammar: Grammar, existingUnitsId: string[] }) {
  const [updatedUnitId, setUpdatedUnitId] = useState<string>(grammar.unit_id);
  const [updatedTitle, setUpdatedTitle] = useState<string>(grammar.title);
  const [updatedExplanation, setUpdatedExplanation] = useState<string>(grammar.explanation);
  const [updatedLearnableSentence, setUpdatedLearnableSentence] = useState<string>(grammar.learnable_sentences?.[0]?.text || "");

  return (
    <form className="flex flex-col space-y-4 items-center">
      <ChangeUnitMenu
        unitsId={existingUnitsId}
        unitId={updatedUnitId}
        onChange={setUpdatedUnitId}
      />
      <AutoWidthInput
        label="Title*"
        value={updatedTitle}
        onChange={(e) => setUpdatedTitle(e.target.value)}
        className="border border-gray-300 rounded-md p-2 h-fit"
      />
      <AutoSizeTextArea
        value={updatedExplanation}
        onChange={(e) => setUpdatedExplanation(e.target.value)}
        label="Explanation"
        className="border border-gray-300 rounded-md p-2 h-fit"
      />
      <AutoWidthInput
        label="Learnable Sentence"
        value={updatedLearnableSentence}
        onChange={(e) => setUpdatedLearnableSentence(e.target.value)}
        className="border border-gray-300 rounded-md p-2 h-fit"
        minWidth={1}
      />
      <UpdateButton
        element={{
          type_element: "gram",
          id: grammar.id,
          title: updatedTitle,
          explanation: updatedExplanation,
          learnable_sentences: updatedLearnableSentence ? [{
            text: updatedLearnableSentence,
            translation: ""
          }] : undefined,
          score: grammar.score,
          last_seen: grammar.last_seen,
          unit_id: updatedUnitId,
        }}
      />
    </form>
  );
}
