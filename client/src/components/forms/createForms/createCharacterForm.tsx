"use client";

import { useState } from "react";

import NewElementButton from "@/components/buttons/newElementButton";
import AutoWidthInput from "@/components/input/autoWidthInput";

export default function createCharacterForm({unit_id}: {unit_id: string}) {
    const [characterName, setCharacterName] = useState<string>("");
    const [components, setComponents] = useState<string>("");
    const [meaning, setMeaning] = useState<string>("");
    const [phonetic, setPhonetic] = useState<string>("");
    const [exampleWord, setExampleWord] = useState<string>("");

  return (
    <form className="flex flex-col space-y-4 items-center">
      <AutoWidthInput
        value={characterName}
        onChange={(e) => setCharacterName(e.target.value)}
        label="Character*"
        className="border border-gray-300 "
      />
      <AutoWidthInput
        value={components}
        onChange={(e) => setComponents(e.target.value)}
        label="Components"
        className="border border-gray-300 "
      />
      <AutoWidthInput
        value={meaning}
        onChange={(e) => setMeaning(e.target.value)}
        label="Meaning*"
        className="border border-gray-300 "
      />
      <AutoWidthInput
        value={phonetic}
        onChange={(e) => setPhonetic(e.target.value)}
        label="Phonetic"
        className="border border-gray-300 "
      />
      <AutoWidthInput
        value={exampleWord}
        onChange={(e) => setExampleWord(e.target.value)}
        label="Example Word"
        className="border border-gray-300 "
      />

      <NewElementButton
        element={{
          type_element: "char",
          id: "",
          character: characterName,
          meaning: meaning,
          components: components,
          phonetic: phonetic,
          example_word: exampleWord,
          score: 0,
          last_seen: new Date(),
          unit_id: unit_id
        }}
      />
    </form>
  );
}
