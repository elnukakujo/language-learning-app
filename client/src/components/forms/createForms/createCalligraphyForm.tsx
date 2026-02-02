"use client";

import { useState } from "react";

import NewElementButton from "@/components/buttons/newElementButton";
import AutoWidthInput from "@/components/input/autoWidthInput";

export default function createCalligraphyForm({unit_id}: {unit_id: string}) {
    const [calligraphyName, setCalligraphyName] = useState<string>("");
    const [components, setComponents] = useState<string>("");
    const [meaning, setMeaning] = useState<string>("");
    const [phonetic, setPhonetic] = useState<string>("");
    const [exampleWord, setExampleWord] = useState<string>("");

  return (
    <form className="flex flex-col space-y-4 items-center">
      <AutoWidthInput
        value={calligraphyName}
        onChange={(e) => setCalligraphyName(e.target.value)}
        label="Calligraphy Character*"
        className="border border-gray-300 "
      />
      <AutoWidthInput
        value={components}
        onChange={(e) => setComponents(e.target.value)}
        label="Radical"
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
          character: {
            character: calligraphyName,
            phonetic: phonetic,
            meaning: meaning,
            radical: components
          },
          example_word: exampleWord ? {
            word: exampleWord,
            translation: ""
          } : undefined,
          unit_id: unit_id
        }}
        type="call"
      />
    </form>
  );
}
