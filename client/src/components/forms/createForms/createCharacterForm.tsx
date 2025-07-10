"use client";

import { useState } from "react";

import NewElementButton from "@/components/buttons/newElementButton";

export default function createCharacterForm({unit_id}: {unit_id: string}) {
    const [characterName, setCharacterName] = useState<string>("");
    const [components, setComponents] = useState<string>("");
    const [meaning, setMeaning] = useState<string>("");
    const [phonetic, setPhonetic] = useState<string>("");
    const [exampleWord, setExampleWord] = useState<string>("");

  return (
    <form className="flex flex-col space-y-4">
      <div className="flex flex-col space-y-2 h-fit">
        {[characterName, components, meaning, phonetic, exampleWord].map((value, index) => (
            <div key={index}>
              <label htmlFor={`field-${index}`} key={index}>
                {["Character*", "Components", "Meaning*", "Phonetic", "Example Word"][index]}
              </label>
              <input
                    key={'char'+index}
                    type="text"
                    value={value}
                    onChange={(e) => {
                        const newValue = e.target.value;
                        if (index === 0) setCharacterName(newValue);
                        if (index === 1) setComponents(newValue);
                        if (index === 2) setMeaning(newValue);
                        if (index === 3) setPhonetic(newValue);
                        if (index === 4) setExampleWord(newValue);
                    }}
                    className="border border-gray-300 rounded p-2 w-full"
                />
            </div>
          ))}
      </div>

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
