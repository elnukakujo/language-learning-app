"use client";

import { useState } from "react";
import UpdateButton from "@/components/buttons/updateButton";
import type Character from "@/interface/Character";

export default function updateCharacterForm({ character }: { character: Character }) {
    const [characterName, setCharacterName] = useState<string>(character.character);
    const [components, setComponents] = useState<string>(character.components || "");
    const [meaning, setMeaning] = useState<string>(character.meaning);
    const [phonetic, setPhonetic] = useState<string>(character.phonetic || "");
    const [exampleWord, setExampleWord] = useState<string>(character.example_word || "");

  return (
    <form className="flex flex-col space-y-4">
      <div className="flex flex-col space-y-2 h-fit">
        {[characterName, components, meaning, phonetic, exampleWord].map((value, index) => (
            <div key={index}>
              <label htmlFor={`field-${index}`} key={index}>
                {["Character Name", "Components", "Meaning", "Phonetic", "Example Word"][index]}
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

      <UpdateButton
        element={{
            type_element: "char",
            id: character.id,
            character: characterName,
            meaning: meaning,
            components: components,
            phonetic: phonetic,
            example_word: exampleWord,
            score: character.score,
            last_seen: character.last_seen,
            unit_id: character.unit_id,
        }}
      />
    </form>
  );
}
