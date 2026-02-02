"use client";

import { useState } from "react";
import UpdateButton from "@/components/buttons/updateButton";
import ChangeUnitMenu from "@/components/selectMenu/changeUnitMenu";
import AutoWidthInput from "@/components/input/autoWidthInput";
import type Character from "@/interface/features/Calligraphy";

export default function updateCalligraphyForm({ calligraphy, existingUnitsId }: { calligraphy: Character, existingUnitsId: string[] }) {
    const [updatedCalligraphyName, setUpdatedCalligraphyName] = useState<string>(calligraphy.character.character);
    const [updatedRadical, setUpdatedRadical] = useState<string>(calligraphy.character.radical || "");
    const [updatedMeaning, setUpdatedMeaning] = useState<string>(calligraphy.character.meaning || "");
    const [updatedPhonetic, setUpdatedPhonetic] = useState<string>(calligraphy.character.phonetic || "");
    const [updatedExampleWord, setUpdatedExampleWord] = useState<string>(calligraphy.example_word?.word || "");
    const [updatedUnitId, setUpdatedUnitId] = useState<string>(calligraphy.unit_id);

  return (
    <form className="flex flex-col space-y-4 items-center">
      <AutoWidthInput
        value={updatedCalligraphyName}
        label="Calligraphy Character"
        onChange={(e) => setUpdatedCalligraphyName(e.target.value)}
        placeholder="Enter calligraphy character"
        className="border border-gray-300"
      />
      <AutoWidthInput
        value={updatedRadical}
        label="Radical"
        onChange={(e) => setUpdatedRadical(e.target.value)}
        placeholder="Enter radical"
        className="border border-gray-300"
      />
      <AutoWidthInput
        value={updatedMeaning}
        label="Meaning"
        onChange={(e) => setUpdatedMeaning(e.target.value)}
        placeholder="Enter meaning"
        className="border border-gray-300"
      />
      <AutoWidthInput
        value={updatedPhonetic}
        label="Phonetic"
        onChange={(e) => setUpdatedPhonetic(e.target.value)}
        placeholder="Enter phonetic"
        className="border border-gray-300"
      />
      <AutoWidthInput
        value={updatedExampleWord}
        label="Example Word"
        onChange={(e) => setUpdatedExampleWord(e.target.value)}
        placeholder="Enter example word"
        className="border border-gray-300"
      />

      <UpdateButton
        element={{
            type_element: "char",
            id: calligraphy.id!,
            character: {
              character: updatedCalligraphyName,
              phonetic: updatedPhonetic,
              meaning: updatedMeaning,
              radical: updatedRadical
            },
            example_word: updatedExampleWord ? {
              word: updatedExampleWord,
              translation: ""
            } : undefined,
            score: calligraphy.score,
            last_seen: calligraphy.last_seen,
            unit_id: updatedUnitId,
        }}
      />
    </form>
  );
}
