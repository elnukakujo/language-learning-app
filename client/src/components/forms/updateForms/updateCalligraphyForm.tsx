"use client";

import { useState } from "react";
import UpdateButton from "@/components/buttons/updateButton";
import AutoWidthInput from "@/components/input/autoWidthInput";
import Calligraphy from "@/interface/features/Calligraphy";
import { updateCalligraphy } from "@/api";
import { useRouter } from "next/dist/client/components/navigation";
import MediaLoader from "@/components/mediaLoader";
import ClassicSelectMenu from "@/components/selectMenu/classicSelectMenu";

export default function updateCalligraphyForm({ calligraphy }: { calligraphy: Calligraphy }) {
    const router = useRouter();
  
    const [updatedCalligraphyName, setUpdatedCalligraphyName] = useState<string | undefined>(calligraphy.character.character || undefined);
    const [updatedPhonetic, setUpdatedPhonetic] = useState<string | undefined>(calligraphy.character.phonetic || undefined);
    const [updatedMeaning, setUpdatedMeaning] = useState<string | undefined>(calligraphy.character.meaning || undefined);
    const [updatedRadical, setUpdatedRadical] = useState<string | undefined>(calligraphy.character.radical || undefined);
    const [updatedImageUrl, setUpdatedImageUrl] = useState<string | undefined>(calligraphy.character.image_files?.[0] || undefined);
    const [updatedAudioUrl, setUpdatedAudioUrl] = useState<string | undefined>(calligraphy.character.audio_files?.[0] || undefined);

    const [updatedExampleWord, setUpdatedExampleWord] = useState<string | undefined>(calligraphy.example_word?.word || undefined);
    const [updatedExampleWordTranslation, setUpdatedExampleWordTranslation] = useState<string|undefined>(calligraphy.example_word?.translation || undefined);
    const [updatedExampleWordType, setUpdatedExampleWordType] = useState<"noun" | "verb" | "adjective" | "adverb" | "pronoun"
    | "article" | "preposition" | "conjunction" | "particle" | "interjection" | "numeral" | "classifier" 
    | "auxiliary" | "modal" | "">(calligraphy.example_word?.type || "");
    const [updatedExampleWordGender, setUpdatedExampleWordGender] = useState<"m" | "f" | "n" | undefined>(calligraphy.example_word?.gender || undefined);
    const [updatedExampleImageUrl, setUpdatedExampleImageUrl] = useState<string | undefined>(calligraphy.example_word?.image_files?.[0] || undefined);
    const [updatedExampleAudioUrl, setUpdatedExampleAudioUrl] = useState<string | undefined>(calligraphy.example_word?.audio_files?.[0] || undefined);

    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        
        // Extract language_id from current URL
        const currentPath = window.location.pathname;
        const pathParts = currentPath.split('/');
        const languageId = pathParts[2]; // From /languages/LANG_ID/...
        
        const element: Calligraphy = {
          character: {
            character: updatedCalligraphyName!,
            phonetic: updatedPhonetic!,
            meaning: updatedMeaning || undefined,
            radical: updatedRadical || undefined,
            image_files: updatedImageUrl ? [updatedImageUrl] : [],
            audio_files: updatedAudioUrl ? [updatedAudioUrl] : []
          },
          example_word: updatedExampleWord ? {
            word: updatedExampleWord,
            translation: updatedExampleWordTranslation || "",
            type: updatedExampleWordType as Exclude<typeof updatedExampleWordType, ''>,
            gender: updatedExampleWordGender,
            image_files: updatedExampleImageUrl ? [updatedExampleImageUrl] : [],
            audio_files: updatedExampleAudioUrl ? [updatedExampleAudioUrl] : []
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
        <MediaLoader imageUrl={updatedImageUrl} setImageUrl={setUpdatedImageUrl} audioUrl={updatedAudioUrl} setAudioUrl={setUpdatedAudioUrl} />
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
        <ClassicSelectMenu
          label="Type of Word"
          options={[
            'noun', 'verb', 'adjective', 'adverb', 'pronoun', 'article', 
            'preposition', 'conjunction', 'particle', 'interjection', 'numeral', 
            'classifier', 'auxiliary', 'modal'
          ]}
          selectedOption={updatedExampleWordType}
          onChange={(value) => setUpdatedExampleWordType(value as typeof updatedExampleWordType)}
        />
        <ClassicSelectMenu
          label="Gender of Word"
          options={[
            'm', 'f', 'n'
          ]}
          selectedOption={updatedExampleWordGender || ""}
          onChange={(value) => setUpdatedExampleWordGender(value as typeof updatedExampleWordGender)}
        />
        <MediaLoader imageUrl={updatedExampleImageUrl} setImageUrl={setUpdatedExampleImageUrl} audioUrl={updatedExampleAudioUrl} setAudioUrl={setUpdatedExampleAudioUrl} />
      </span>

      <UpdateButton>Update Calligraphy</UpdateButton>
    </form>
  );
}
