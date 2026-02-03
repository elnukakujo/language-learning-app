"use client";

import { useState } from "react";
import UpdateButton from "@/components/buttons/updateButton";
import AutoWidthInput from "@/components/input/autoWidthInput";
import Calligraphy from "@/interface/features/Calligraphy";
import { updateCalligraphy } from "@/api";
import { useRouter } from "next/dist/client/components/navigation";

export default function updateCalligraphyForm({ calligraphy }: { calligraphy: Calligraphy }) {
    const router = useRouter();
  
    const [updatedCalligraphyName, setUpdatedCalligraphyName] = useState<string | undefined>(calligraphy.character.character || undefined);
    const [updatedPhonetic, setUpdatedPhonetic] = useState<string | undefined>(calligraphy.character.phonetic || undefined);
    const [updatedMeaning, setUpdatedMeaning] = useState<string | undefined>(calligraphy.character.meaning || undefined);
    const [updatedRadical, setUpdatedRadical] = useState<string | undefined>(calligraphy.character.radical || undefined);
    const [updatedExampleWord, setUpdatedExampleWord] = useState<string | undefined>(calligraphy.example_word?.word || undefined);
    const [updatedExampleWordTranslation, setUpdatedExampleWordTranslation] = useState<string|undefined>(calligraphy.example_word?.translation || undefined);

    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        
        // Extract language_id from current URL
        const currentPath = window.location.pathname;
        const pathParts = currentPath.split('/');
        const languageId = pathParts[2]; // From /languages/LANG_ID/...
        
        const element = {
          character: {
            character: updatedCalligraphyName,
            phonetic: updatedPhonetic,
            meaning: updatedMeaning || undefined,
            radical: updatedRadical || undefined
          },
          example_word: updatedExampleWord ? {
            word: updatedExampleWord,
            translation: updatedExampleWordTranslation || undefined
          } : undefined,
          unit_id: calligraphy.unit_id
        };
        
        try {
          await updateCalligraphy(calligraphy.id!, element);
          
          const router_path = `/languages/${languageId}/unit/${calligraphy.unit_id}/call/${calligraphy.id}/`;
          
          router.push(router_path);
          router.refresh();
          
        } catch (error) {
          console.error("Failed to update calligraphy:", error);
          alert("Failed to update calligraphy. Check console for details.");
        }
      };

  return (
    <form className="flex flex-col space-y-12" onSubmit={handleSubmit}>
      <span className="flex flex-col space-y-2 items-center">
        <h3>Character Informations</h3>
        <AutoWidthInput
          value={updatedCalligraphyName || ""}
          onChange={(e) => setUpdatedCalligraphyName(e.target.value)}
          label="Calligraphy Character"
          className="border border-gray-300"
          required={true}
        />
        <AutoWidthInput
          value={updatedPhonetic || ""}
          onChange={(e) => setUpdatedPhonetic(e.target.value)}
          label="Phonetic"
          className="border border-gray-300"
          required={true}
        />
        <AutoWidthInput
          value={updatedRadical || ""}
          onChange={(e) => setUpdatedRadical(e.target.value)}
          label="Radical"
          className="border border-gray-300"

        />
        <AutoWidthInput
          value={updatedMeaning || ""}
          onChange={(e) => setUpdatedMeaning(e.target.value)}
          label="Meaning"
          className="border border-gray-300"
        />
      </span>
      <span className="flex flex-col space-y-2 items-center">
        <h3>Example Word Informations</h3>
        <AutoWidthInput
          value={updatedExampleWord || ""}
          onChange={(e) => setUpdatedExampleWord(e.target.value)}
          label="Example Word"
          className="border border-gray-300"
        />
          <AutoWidthInput
          value={updatedExampleWordTranslation || ""}
          onChange={(e) => setUpdatedExampleWordTranslation(e.target.value)}
          label="Example Word Translation"
          className="border border-gray-300"
        />
      </span>

      <UpdateButton>Update Calligraphy</UpdateButton>
    </form>
  );
}
