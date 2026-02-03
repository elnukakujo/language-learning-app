"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";
import NewElementButton from "@/components/buttons/newElementButton";
import AutoWidthInput from "@/components/input/autoWidthInput";
import { createCalligraphy } from "@/api";

export default function CreateCalligraphyForm({unit_id}: {unit_id: string}) {
  const router = useRouter();
  
  const [calligraphyName, setCalligraphyName] = useState<string|undefined>(undefined);
  const [components, setComponents] = useState<string|undefined>(undefined);
  const [meaning, setMeaning] = useState<string|undefined>(undefined);
  const [phonetic, setPhonetic] = useState<string|undefined>(undefined);
  const [exampleWord, setExampleWord] = useState<string|undefined>(undefined);
  const [exampleWordTranslation, setExampleWordTranslation] = useState<string|undefined>(undefined);

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    
    // Extract language_id from current URL
    const currentPath = window.location.pathname;
    const pathParts = currentPath.split('/');
    const languageId = pathParts[2]; // From /languages/LANG_ID/...
    
    const element = {
      character: {
        character: calligraphyName,
        phonetic: phonetic,
        meaning: meaning || undefined,
        radical: components || undefined
      },
      example_word: exampleWord ? {
        word: exampleWord,
        translation: exampleWordTranslation || undefined
      } : undefined,
      unit_id: unit_id
    };
    
    try {
      await createCalligraphy(element);
      
      const router_path = `/languages/${languageId}/unit/${unit_id}`;
      
      router.push(router_path);
      router.refresh();
      
    } catch (error) {
      console.error("Failed to create calligraphy:", error);
      alert("Failed to create calligraphy. Check console for details.");
    }
  };

  return (
    <form className="flex flex-col space-y-12" onSubmit={handleSubmit}>
      <span className="flex flex-col space-y-2 items-center">
        <h3>Character Informations</h3>
        <AutoWidthInput
          value={calligraphyName || ""}
          onChange={(e) => setCalligraphyName(e.target.value)}
          label="Calligraphy Character"
          className="border border-gray-300"
          required={true}
        />
        <AutoWidthInput
          value={phonetic || ""}
          onChange={(e) => setPhonetic(e.target.value)}
          label="Phonetic"
          className="border border-gray-300"
          required={true}
        />
        <AutoWidthInput
          value={meaning || ""}
          onChange={(e) => setMeaning(e.target.value)}
          label="Meaning"
          className="border border-gray-300"
        />
        <AutoWidthInput
          value={components || ""}
          onChange={(e) => setComponents(e.target.value)}
          label="Radical"
          className="border border-gray-300"
        />
      </span>
      <span className="flex flex-col space-y-2 items-center">
        <h3>Example Word Informations</h3>
        <AutoWidthInput
          value={exampleWord || ""}
          onChange={(e) => setExampleWord(e.target.value)}
          label="Example Word"
          className="border border-gray-300"
        />
          <AutoWidthInput
          value={exampleWordTranslation || ""}
          onChange={(e) => setExampleWordTranslation(e.target.value)}
          label="Example Word Translation"
          className="border border-gray-300"
        />
      </span>
      <NewElementButton>Add Calligraphy</NewElementButton>
    </form>
  );
}