"use client";

import { useState } from "react";
import UpdateButton from "@/components/buttons/updateButton";
import type Vocabulary from "@/interface/Vocabulary";

export default function updateVocabularyForm({ vocabulary }: { vocabulary: Vocabulary }) {
    const [word, setWord] = useState<string>(vocabulary.word);
    const [translation, setTranslation] = useState<string>(vocabulary.translation);
    const [phonetic, setPhonetic] = useState<string | undefined>(vocabulary.phonetic);
    const [type, setType] = useState<string | undefined>(vocabulary.type);
    const [example_sentence, setExampleSentence] = useState<string | undefined>(vocabulary.example_sentence);

  return (
    <form className="flex flex-col space-y-4">
      <div className="flex flex-col space-y-2 h-fit">
        {[word, translation, type, phonetic, example_sentence].map((value, index) => (
            <div key={index}>
              <label htmlFor={`field-${index}`} key={index}>
                {["Word", "Translation", "Type", "Phonetic", "Example Sentence"][index]}
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

      <UpdateButton
        element={{
            type_element: "voc",
            id: vocabulary.id,
            word: word,
            translation: translation,
            phonetic: phonetic,
            type: type,
            example_sentence: example_sentence,          
            score: vocabulary.score,
            last_seen: vocabulary.last_seen,
            unit_id: vocabulary.unit_id,
        }}
      />
    </form>
  );
}
