"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";
import NewElementButton from "@/components/buttons/newElementButton";
import AutoWidthInput from "@/components/input/autoWidthInput";
import { createCalligraphy } from "@/api";
import MediaLoader from "@/components/mediaLoader";
import Calligraphy from "@/interface/features/Calligraphy";
import ClassicSelectMenu from "@/components/selectMenu/classicSelectMenu";

export default function CreateCalligraphyForm({unit_id}: {unit_id: string}) {
  const router = useRouter();
  
  const [calligraphyName, setCalligraphyName] = useState<string|undefined>(undefined);
  const [components, setComponents] = useState<string|undefined>(undefined);
  const [meaning, setMeaning] = useState<string|undefined>(undefined);
  const [phonetic, setPhonetic] = useState<string|undefined>(undefined);
  const [imageUrl, setImageUrl] = useState<string|undefined>(undefined);
  const [audioUrl, setAudioUrl] = useState<string|undefined>(undefined);

  const [exampleWord, setExampleWord] = useState<string|undefined>(undefined);
  const [exampleWordTranslation, setExampleWordTranslation] = useState<string|undefined>(undefined);
  const [exampleWordType, setExampleWordType] = useState<"noun" | "verb" | "adjective" | "adverb" | "pronoun"
  | "article" | "preposition" | "conjunction" | "particle" | "interjection" | "numeral" | "classifier" 
  | "auxiliary" | "modal" | "">("");
  const [exampleWordGender, setExampleWordGender] = useState<"m" | "f" | "n" | undefined>(undefined);
  const [exampleImageUrl, setExampleImageUrl] = useState<string|undefined>(undefined);
  const [exampleAudioUrl, setExampleAudioUrl] = useState<string|undefined>(undefined);

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    
    // Extract language_id from current URL
    const currentPath = window.location.pathname;
    const pathParts = currentPath.split('/');
    const languageId = pathParts[2]; // From /languages/LANG_ID/...
    
    const element: Calligraphy = {
      character: {
        character: calligraphyName!,
        phonetic: phonetic!,
        meaning: meaning || undefined,
        radical: components || undefined,
        image_files: imageUrl ? [imageUrl] : [],
        audio_files: audioUrl ? [audioUrl] : []
      },
      example_word: exampleWord ? {
        word: exampleWord,
        translation: exampleWordTranslation || "",
        type: exampleWordType as Exclude<typeof exampleWordType, ''>,
        gender: exampleWordGender,
        image_files: exampleImageUrl ? [exampleImageUrl] : [],
        audio_files: exampleAudioUrl ? [exampleAudioUrl] : []
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
        <MediaLoader imageUrl={imageUrl} setImageUrl={setImageUrl} audioUrl={audioUrl} setAudioUrl={setAudioUrl} />
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
        <ClassicSelectMenu
          label="Type of Word"
          options={[
            'noun', 'verb', 'adjective', 'adverb', 'pronoun', 'article', 
            'preposition', 'conjunction', 'particle', 'interjection', 'numeral', 
            'classifier', 'auxiliary', 'modal'
          ]}
          selectedOption={exampleWordType}
          onChange={(value) => setExampleWordType(value as typeof exampleWordType)}
        />
        <ClassicSelectMenu
          label="Gender of Word"
          options={[
            'm', 'f', 'n'
          ]}
          selectedOption={exampleWordGender || ""}
          onChange={(value) => setExampleWordGender(value as typeof exampleWordGender)}
        />
        <MediaLoader imageUrl={exampleImageUrl} setImageUrl={setExampleImageUrl} audioUrl={exampleAudioUrl} setAudioUrl={setExampleAudioUrl} />
      </span>
      <NewElementButton>Add Calligraphy</NewElementButton>
    </form>
  );
}