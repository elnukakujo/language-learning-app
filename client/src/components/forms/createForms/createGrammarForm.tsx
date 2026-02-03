"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";
import NewElementButton from "@/components/buttons/newElementButton";
import AutoWidthInput from "@/components/input/autoWidthInput";
import AutoSizeTextArea from "@/components/textArea/autoSizeTextArea";
import { createGrammar } from "@/api";

export default function CreateGrammarForm({unit_id}: {unit_id: string}) {
  const router = useRouter();
  
  const [title, setTitle] = useState<string | undefined>(undefined);
  const [explanation, setExplanation] = useState<string | undefined>(undefined);
  const [learnableSentence, setLearnableSentence] = useState<string | undefined>(undefined);
  const [learnableSentenceTranslation, setLearnableSentenceTranslation] = useState<string | undefined>(undefined);

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    
    // Extract language_id from current URL
    const currentPath = window.location.pathname;
    const pathParts = currentPath.split('/');
    const languageId = pathParts[2]; // From /languages/LANG_ID/...
    
    const element = {
      title: title,
      explanation: explanation,
      learnable_sentences: learnableSentence ? [{
        text: learnableSentence,
        translation: learnableSentenceTranslation || undefined
      }] : undefined,
      unit_id: unit_id
    };
    
    try {
      await createGrammar(element);
      
      const router_path = `/languages/${languageId}/unit/${unit_id}`;
      
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
          value={title || ""}
          onChange={(e) => setTitle(e.target.value)}
          className="border border-gray-300"
          required={true}
        />
        <AutoSizeTextArea
          value={explanation || ""}
          onChange={(e) => setExplanation(e.target.value)}
          label="Explanation"
          required={true}
        />
      </span>
      <span className="flex flex-col space-y-2 items-center">
        <h3>Learnable Sentence Informations</h3>
        <AutoWidthInput
          label="Learnable Sentence"
          value={learnableSentence || ""}
          onChange={(e) => setLearnableSentence(e.target.value)}
          className="border border-gray-300"
        />
        <AutoWidthInput
          label="Learnable Sentence Translation"
          value={learnableSentenceTranslation || ""}
          onChange={(e) => setLearnableSentenceTranslation(e.target.value)}
          className="border border-gray-300"
        />
      </span>
      <NewElementButton>Add Grammar</NewElementButton>
    </form>
  );
}