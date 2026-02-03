"use client";

import { useState } from "react";
import UpdateButton from "@/components/buttons/updateButton";
import ChangeUnitMenu from "@/components/selectMenu/changeUnitMenu";
import type Grammar from "@/interface/features/Grammar";
import AutoWidthInput from "@/components/input/autoWidthInput";
import AutoSizeTextArea from "@/components/textArea/autoSizeTextArea";
import { useRouter } from "next/navigation";
import { updateGrammar } from "@/api";

export default function updateGrammarForm({ grammar }: { grammar: Grammar }) {
  const router = useRouter();
  const [updatedTitle, setUpdatedTitle] = useState<string | undefined>(grammar.title || undefined);
  const [updatedExplanation, setUpdatedExplanation] = useState<string | undefined>(grammar.explanation || undefined);
  const [updatedLearnableSentence, setUpdatedLearnableSentence] = useState<string | undefined>(grammar.learnable_sentences?.[0]?.text || undefined);
  const [updatedLearnableSentenceTranslation, setUpdatedLearnableSentenceTranslation] = useState<string | undefined>(grammar.learnable_sentences?.[0]?.translation || "");

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
      e.preventDefault();
      
      // Extract language_id from current URL
      const currentPath = window.location.pathname;
      const pathParts = currentPath.split('/');
      const languageId = pathParts[2]; // From /languages/LANG_ID/...
      
      const element = {
        title: updatedTitle,
        explanation: updatedExplanation,
        learnable_sentences: updatedLearnableSentence ? [{
          text: updatedLearnableSentence,
          translation: updatedLearnableSentenceTranslation || undefined
        }] : undefined,
        unit_id: grammar.unit_id
      };
      
      try {
        await updateGrammar(grammar.id!, element);
        
        const router_path = `/languages/${languageId}/unit/${grammar.unit_id}/gram/${grammar.id}/`;
        
        router.push(router_path);
        router.refresh();
        
      } catch (error) {
        console.error("Failed to create grammar:", error);
        alert("Failed to create grammar. Check console for details.");
      }
    };

  return (
    <form className="flex flex-col space-y-12" onSubmit={handleSubmit}>
      <span className="flex flex-col space-y-2 items-center">
        <h3>Grammar Informations</h3>
        <AutoWidthInput
          label="Title"
          value={updatedTitle || ""}
          onChange={(e) => setUpdatedTitle(e.target.value)}
          className="border border-gray-300"
          required={true}
        />
        <AutoSizeTextArea
          value={updatedExplanation || ""}
          onChange={(e) => setUpdatedExplanation(e.target.value)}
          label="Explanation"
          required={true}
        />
      </span>
      <span className="flex flex-col space-y-2 items-center">
        <h3>Learnable Sentence Informations</h3>
        <AutoWidthInput
          label="Learnable Sentence"
          value={updatedLearnableSentence || ""}
          onChange={(e) => setUpdatedLearnableSentence(e.target.value)}
          className="border border-gray-300"
        />
        <AutoWidthInput
          label="Learnable Sentence Translation"
          value={updatedLearnableSentenceTranslation || ""}
          onChange={(e) => setUpdatedLearnableSentenceTranslation(e.target.value)}
          className="border border-gray-300"
        />
      </span>
      <UpdateButton>Update Grammar</UpdateButton>
    </form>
  );
}
