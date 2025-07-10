"use client";

import { useState } from "react";
import NewElementButton from "@/components/buttons/newElementButton";

export default function createVocabularyForm({ unit_id }: { unit_id: string }) {
    const [word, setWord] = useState<string>("");
    const [translation, setTranslation] = useState<string>("");
    const [phonetic, setPhonetic] = useState<string | undefined>("");
    const [type, setType] = useState<string | undefined>("");
    const [example_sentence, setExampleSentence] = useState<string | undefined>("");

  return (
    <form className="flex flex-col space-y-4">
      <div className="flex flex-col space-y-2 h-fit">
        {[word, translation, type, phonetic, example_sentence].map((value, index) => (
            <div key={index}>
              <label htmlFor={`field-${index}`} key={index}>
                {["Word*", "Translation*", "Type", "Phonetic", "Example Sentence"][index]}
              </label>
              <input
                    key={'voc'+index}
                    type="text"
                    value={value}
                    onChange={(e) => {
                        const newValue = e.target.value;
                        if (index === 0) setWord(newValue);
                        if (index === 1) setTranslation(newValue);
                        if (index === 2) setPhonetic(newValue);
                        if (index === 3) setType(newValue);
                        if (index === 4) setExampleSentence(newValue);
                    }}
                    className="border border-gray-300 rounded p-2 w-full"
                />
            </div>
          ))}
      </div>

      <NewElementButton
        element={{
            type_element: "voc",
            id: "",
            word: word,
            translation: translation,
            phonetic: phonetic,
            type: type,
            example_sentence: example_sentence,          
            score: 0.0,
            last_seen: new Date(),
            unit_id: unit_id
        }}
      />
    </form>
  );
}
