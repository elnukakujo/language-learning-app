"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";
import NewElementButton from "@/components/buttons/newElementButton";
import AutoWidthInput from "@/components/input/autoWidthInput";
import ClassicSelectMenu from "@/components/selectMenu/classicSelectMenu";
import { createVocabulary } from "@/api";
import MediaLoader from "@/components/mediaLoader";
import Vocabulary from "@/interface/features/Vocabulary";

export default function CreateVocabularyForm({ unit_id }: { unit_id: string }) {
  const router = useRouter();
  
  const [word, setWord] = useState<string>("");
  const [translation, setTranslation] = useState<string>("");
  const [phonetic, setPhonetic] = useState<string>("");
  const [type, setType] = useState<'noun' | 'verb' | 'adjective' | 'adverb' | 'pronoun' | 'article' | 
    'preposition' | 'conjunction' | 'particle' | 'interjection' | 'numeral' | 
    'classifier' | 'auxiliary' | 'modal' | ''>("");
  const [wordImageUrl, setWordImageUrl] = useState<string | undefined>(undefined);
  const [wordAudioUrl, setWordAudioUrl] = useState<string | undefined>(undefined);

  const [example_sentence, setExampleSentence] = useState<string>("");
  const [example_sentence_translation, setExampleSentenceTranslation] = useState<string>("");
  const [exampleImageUrl, setExampleImageUrl] = useState<string | undefined>(undefined);
  const [exampleAudioUrl, setExampleAudioUrl] = useState<string | undefined>(undefined);

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    
    // Extract language_id from current URL
    const currentPath = window.location.pathname;
    const pathParts = currentPath.split('/');
    const languageId = pathParts[2]; // From /languages/LANG_ID/...
    
    const element: Vocabulary = {
      word: {
        word: word,
        translation: translation,
        type: type as Exclude<typeof type, ''>,
        phonetic: phonetic || undefined,
        image_files: wordImageUrl ? [wordImageUrl] : [],
        audio_files: wordAudioUrl ? [wordAudioUrl] : []
      },
      example_sentences: example_sentence ? [{
        text: example_sentence,
        translation: example_sentence_translation || "",
        image_files: exampleImageUrl ? [exampleImageUrl] : [],
        audio_files: exampleAudioUrl ? [exampleAudioUrl] : []
      }] : undefined,          
      unit_id: unit_id
    };
    
    try {
      await createVocabulary(element);
      
      const router_path = `/languages/${languageId}/unit/${unit_id}`;
      
      router.push(router_path);
      router.refresh();
      
    } catch (error) {
      console.error("Failed to create vocabulary:", error);
      alert("Failed to create vocabulary. Check console for details.");
    }
  };

  return (
    <form 
      className="flex flex-col space-y-12" 
      onSubmit={handleSubmit}
    >
      <span className="flex flex-col space-y-2 items-center">
        <h3> Word Informations </h3>
        <AutoWidthInput
          value={word}
          label="Word"
          onChange={(e) => setWord(e.target.value)}
          placeholder="Enter word"
          className="border border-gray-300"
          required={true}
        />
        <AutoWidthInput
          value={translation}
          label="Translation"
          onChange={(e) => setTranslation(e.target.value)}
          placeholder="Enter translation"
          className="border border-gray-300"
          required={true}
        />
        <ClassicSelectMenu
          label="Type of Word"
          options={[
            'noun', 'verb', 'adjective', 'adverb', 'pronoun', 'article', 
            'preposition', 'conjunction', 'particle', 'interjection', 'numeral', 
            'classifier', 'auxiliary', 'modal'
          ]}
          selectedOption={type}
          onChange={(value) => setType(value as typeof type)}
          required={true}
        />
        <AutoWidthInput
          value={phonetic}
          label="Phonetic"
          onChange={(e) => setPhonetic(e.target.value)}
          placeholder="Enter phonetic"
          className="border border-gray-300"
        />
        <MediaLoader imageUrl={wordImageUrl} setImageUrl={setWordImageUrl} audioUrl={wordAudioUrl} setAudioUrl={setWordAudioUrl} />
      </span>
      
      <span className="flex flex-col space-y-4 items-center">
        <h3> Example Sentence Informations </h3>
        <AutoWidthInput
          value={example_sentence}
          label="Example Sentence"
          onChange={(e) => setExampleSentence(e.target.value)}
          placeholder="Enter example sentence"
          className="border border-gray-300"
        />
        <AutoWidthInput
          value={example_sentence_translation}
          label="Example Sentence Translation"
          onChange={(e) => setExampleSentenceTranslation(e.target.value)}
          placeholder="Enter example sentence translation"
          className="border border-gray-300"
        />
        <MediaLoader imageUrl={exampleImageUrl} setImageUrl={setExampleImageUrl} audioUrl={exampleAudioUrl} setAudioUrl={setExampleAudioUrl} />
      </span>
      
      <NewElementButton>Add Vocabulary</NewElementButton>
    </form>
  );
}