"use client";

import { useState } from "react";
import UpdateButton from "@/components/buttons/updateButton";
import ChangeUnitMenu from "@/components/selectMenu/changeUnitMenu";
import AutoWidthInput from "@/components/input/autoWidthInput";
import type Character from "@/interface/Character";

export default function updateCharacterForm({ character, existingUnitsId }: { character: Character, existingUnitsId: string[] }) {
    const [updatedCharacterName, setUpdatedCharacterName] = useState<string>(character.character);
    const [updatedComponents, setUpdatedComponents] = useState<string>(character.components || "");
    const [updatedMeaning, setUpdatedMeaning] = useState<string>(character.meaning);
    const [updatedPhonetic, setUpdatedPhonetic] = useState<string>(character.phonetic || "");
    const [updatedExampleWord, setUpdatedExampleWord] = useState<string>(character.example_word || "");
    const [updatedUnitId, setUpdatedUnitId] = useState<string>(character.unit_id);

  return (
    <form className="flex flex-col space-y-4 items-center">
      <AutoWidthInput
        value={updatedCharacterName}
        label="Character Name"
        onChange={(e) => setUpdatedCharacterName(e.target.value)}
        placeholder="Enter character name"
        className="border border-gray-300"
      />
      <AutoWidthInput
        value={updatedComponents}
        label="Components"
        onChange={(e) => setUpdatedComponents(e.target.value)}
        placeholder="Enter components"
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
            id: character.id,
            character: updatedCharacterName,
            meaning: updatedMeaning,
            components: updatedComponents,
            phonetic: updatedPhonetic,
            example_word: updatedExampleWord,
            score: character.score,
            last_seen: character.last_seen,
            unit_id: updatedUnitId,
        }}
      />
    </form>
  );
}
