"use client";

import { useState } from "react";
import UpdateButton from "@/components/buttons/updateButton";
import ChangeUnitMenu from "@/components/selectMenu/changeUnitMenu";
import type Vocabulary from "@/interface/features/Vocabulary";
import AutoWidthInput from "@/components/input/autoWidthInput";

export default function updateVocabularyForm({ vocabulary, existingUnitsId }: { vocabulary: Vocabulary, existingUnitsId: string[] }) {
    const [updatedWord, setUpdatedWord] = useState<string>(vocabulary.word.word);
    const [updatedTranslation, setUpdatedTranslation] = useState<string>(vocabulary.word.translation);
    const [updatedPhonetic, setUpdatedPhonetic] = useState<string>(vocabulary.word.phonetic || "");
    const [updatedType, setUpdatedType] = useState<string>(vocabulary.word.type || "");
    const [updatedExampleSentence, setUpdatedExampleSentence] = useState<string>(vocabulary.example_sentences?.[0]?.text || "");
    const [updatedUnitId, setUpdatedUnitId] = useState<string>(vocabulary.unit_id || "");

    return (
      <form className="flex flex-col space-y-4">
        <ChangeUnitMenu unitsId={existingUnitsId} unitId={updatedUnitId} onChange={setUpdatedUnitId} />
        <AutoWidthInput
          value={updatedWord}
          label="Word"
          onChange={(e) => setUpdatedWord(e.target.value)}
          placeholder="Enter word"
          className="border border-gray-300"
        />
        <AutoWidthInput
          value={updatedTranslation}
          label="Translation"
          onChange={(e) => setUpdatedTranslation(e.target.value)}
          placeholder="Enter translation"
          className="border border-gray-300"
        />
        <AutoWidthInput
          value={updatedType}
          label="Type"
          onChange={(e) => setUpdatedType(e.target.value)}
          placeholder="Enter type"
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
          value={updatedExampleSentence}
          label="Example Sentence"
          onChange={(e) => setUpdatedExampleSentence(e.target.value)}
          placeholder="Enter example sentence"
          className="border border-gray-300"
        />

        <UpdateButton
          element={{
              type_element: "voc",
              id: vocabulary.id,
              word: {
                word: updatedWord,
                translation: updatedTranslation,
                phonetic: updatedPhonetic || undefined,
                type: updatedType || undefined
              },
              example_sentences: updatedExampleSentence ? [{
                text: updatedExampleSentence,
                translation: ""
              }] : undefined,
              score: vocabulary.score,
              last_seen: vocabulary.last_seen,
              unit_id: updatedUnitId,
          }}
        />
      </form>
    );
}
