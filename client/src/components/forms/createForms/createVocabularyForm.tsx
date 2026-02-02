"use client";

import { useState } from "react";
import NewElementButton from "@/components/buttons/newElementButton";
import AutoWidthInput from "@/components/input/autoWidthInput";

export default function createVocabularyForm({ unit_id }: { unit_id: string }) {
  const [word, setWord] = useState<string>("");
  const [translation, setTranslation] = useState<string>("");
  const [phonetic, setPhonetic] = useState<string>("");
  const [type, setType] = useState<string>("");
  const [example_sentence, setExampleSentence] = useState<string>("");

  return (
    <form className="flex flex-col space-y-4 items-center">
      <AutoWidthInput
          value={word}
          label="Word"
          onChange={(e) => setWord(e.target.value)}
          placeholder="Enter word"
          className="border border-gray-300"
      />
      <AutoWidthInput
          value={translation}
          label="Translation"
          onChange={(e) => setTranslation(e.target.value)}
          placeholder="Enter translation"
          className="border border-gray-300"
      />
      <AutoWidthInput
          value={type}
          label="Type"
          onChange={(e) => setType(e.target.value)}
          placeholder="Enter type"
          className="border border-gray-300"
      />
      <AutoWidthInput
          value={phonetic}
          label="Phonetic"
          onChange={(e) => setPhonetic(e.target.value)}
          placeholder="Enter phonetic"
          className="border border-gray-300"
      />
      <AutoWidthInput
          value={example_sentence}
          label="Example Sentence"
          onChange={(e) => setExampleSentence(e.target.value)}
          placeholder="Enter example sentence"
          className="border border-gray-300"
      />
      <NewElementButton
        element={{
            word: {
              word: word,
              translation: translation,
              phonetic: phonetic || undefined,
              type: type || undefined
            },
            example_sentences: example_sentence ? [{
              text: example_sentence,
              translation: ""
            }] : undefined,          
            score: 0.0,
            last_seen: new Date().toISOString(),
            unit_id: unit_id
        }}
        type="voc"
      />
    </form>
  );
}
