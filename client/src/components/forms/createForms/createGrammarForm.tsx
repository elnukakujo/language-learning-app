"use client";

import { useState } from "react";

import NewElementButton from "@/components/buttons/newElementButton";
import AutoWidthInput from "@/components/input/autoWidthInput";
import AutoSizeTextArea from "@/components/textArea/autoSizeTextArea";

export default function createGrammarForm({unit_id}: {unit_id: string}) {
    const [title, setTitle] = useState<string>("");
    const [explanation, setExplanation] = useState<string>("");
    const [learnableSentence, setLearnableSentence] = useState<string>("");
    return (
      <form className="flex flex-col space-y-4 items-center">
        <AutoWidthInput
          label="Title*"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          className="border border-gray-300"
        />
        <AutoSizeTextArea
          value={explanation}
          onChange={(e) => setExplanation(e.target.value)}
          label="Explanation"
        />
        <AutoWidthInput
          label="Learnable Sentence"
          value={learnableSentence}
          onChange={(e) => setLearnableSentence(e.target.value)}
          className="border border-gray-300"
        />
        <NewElementButton
          element={{
            title: title,
            explanation: explanation,
            learnable_sentences: learnableSentence ? [{
              text: learnableSentence,
              translation: ""
            }] : undefined,
            score: 0,
            last_seen: new Date().toISOString(),
            unit_id: unit_id
          }}
          type="gram"
        />
    </form>
  );
}
