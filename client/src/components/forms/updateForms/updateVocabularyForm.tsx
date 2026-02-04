"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";
import UpdateButton from "@/components/buttons/updateButton";
import type Vocabulary from "@/interface/features/Vocabulary";
import AutoWidthInput from "@/components/input/autoWidthInput";
import { updateVocabulary } from "@/api";
import ClassicSelectMenu from "@/components/selectMenu/classicSelectMenu";
import MediaLoader from "@/components/mediaLoader";

export default function updateVocabularyForm({ vocabulary }: { vocabulary: Vocabulary }) {
    const router = useRouter();

    const [updatedWord, setUpdatedWord] = useState<string | undefined>(vocabulary.word.word || undefined);
    const [updatedTranslation, setUpdatedTranslation] = useState<string | undefined>(vocabulary.word.translation || undefined);
    const [updatedPhonetic, setUpdatedPhonetic] = useState<string | undefined>(vocabulary.word.phonetic || undefined);
    const [updatedType, setUpdatedType] = useState<'noun' | 'verb' | 'adjective' | 'adverb' | 'pronoun' | 'article' | 
    'preposition' | 'conjunction' | 'particle' | 'interjection' | 'numeral' | 
    'classifier' | 'auxiliary' | 'modal' | ''>(vocabulary.word.type || "");
    const [updatedWordImageUrl, setUpdatedWordImageUrl] = useState<string | undefined>(vocabulary.word.image_files?.[0] || undefined);
    const [updatedWordAudioUrl, setUpdatedWordAudioUrl] = useState<string | undefined>(vocabulary.word.audio_files?.[0] || undefined);

    const [updatedExampleSentence, setUpdatedExampleSentence] = useState<string | undefined>(vocabulary.example_sentences?.[0]?.text || undefined);
    const [updatedExampleSentenceTranslation, setUpdatedExampleSentenceTranslation] = useState<string | undefined>(vocabulary.example_sentences?.[0]?.translation || undefined);
    const [updatedExampleImageUrl, setUpdatedExampleImageUrl] = useState<string | undefined>(vocabulary.example_sentences?.[0]?.image_files?.[0] || undefined);
    const [updatedExampleAudioUrl, setUpdatedExampleAudioUrl] = useState<string | undefined>(vocabulary.example_sentences?.[0]?.audio_files?.[0] || undefined);

    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
      e.preventDefault();
      
      // Extract language_id from current URL
      const currentPath = window.location.pathname;
      const pathParts = currentPath.split('/');
      const languageId = pathParts[2]; // From /languages/LANG_ID/...
      
      const element: Vocabulary = {
        word: {
          word: updatedWord!,
          translation: updatedTranslation!,
          type: updatedType as Exclude<typeof updatedType, ''>,
          phonetic: updatedPhonetic || undefined,
          image_files: updatedWordImageUrl ? [updatedWordImageUrl] : [],
          audio_files: updatedWordAudioUrl ? [updatedWordAudioUrl] : []
        },
        example_sentences: updatedExampleSentence ? [{
          text: updatedExampleSentence,
          translation: updatedExampleSentenceTranslation || "",
          image_files: updatedExampleImageUrl ? [updatedExampleImageUrl] : [],
          audio_files: updatedExampleAudioUrl ? [updatedExampleAudioUrl] : []
        }] : undefined,          
        unit_id: vocabulary.unit_id
      };
      
      try {
        await updateVocabulary(vocabulary.id!, element);
        
        const router_path = `/languages/${languageId}/unit/${vocabulary.unit_id}/voc/${vocabulary.id}/`;
        
        router.push(router_path);
        router.refresh();
        
      } catch (error) {
        console.error("Failed to update vocabulary:", error);
        alert("Failed to update vocabulary. Check console for details.");
      }
    };
    
    return (
      <form 
        className="flex flex-col space-y-4" 
        onSubmit={handleSubmit}
      >
        <span className="flex flex-col space-y-2 items-center">
          <h3> Word Informations </h3>
          <AutoWidthInput
            value={updatedWord || ""}
            label="Word"
            onChange={(e) => setUpdatedWord(e.target.value)}
            placeholder="Enter word"
            className="border border-gray-300"
            required={true}
          />
          <AutoWidthInput
            value={updatedTranslation || ""}
            label="Translation"
            onChange={(e) => setUpdatedTranslation(e.target.value)}
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
            selectedOption={updatedType}
            onChange={(value) => setUpdatedType(value as typeof updatedType)}
            required={true}
          />
          <AutoWidthInput
            value={updatedPhonetic || ""}
            label="Phonetic"
            onChange={(e) => setUpdatedPhonetic(e.target.value)}
            placeholder="Enter phonetic"
            className="border border-gray-300"
          />
          <MediaLoader imageUrl={updatedWordImageUrl} setImageUrl={setUpdatedWordImageUrl} audioUrl={updatedWordAudioUrl} setAudioUrl={setUpdatedWordAudioUrl} />
        </span>
        
        <span className="flex flex-col space-y-4 items-center">
          <h3> Example Sentence Informations </h3>
          <AutoWidthInput
            value={updatedExampleSentence || ""}
            label="Example Sentence"
            onChange={(e) => setUpdatedExampleSentence(e.target.value)}
            placeholder="Enter example sentence"
            className="border border-gray-300"
          />
          <AutoWidthInput
            value={updatedExampleSentenceTranslation || ""}
            label="Example Sentence Translation"
            onChange={(e) => setUpdatedExampleSentenceTranslation(e.target.value)}
            placeholder="Enter example sentence translation"
            className="border border-gray-300"
          />
          <MediaLoader imageUrl={updatedExampleImageUrl} setImageUrl={setUpdatedExampleImageUrl} audioUrl={updatedExampleAudioUrl} setAudioUrl={setUpdatedExampleAudioUrl} />
        </span>
        <UpdateButton> Update Vocabulary</UpdateButton>
      </form>
    );
}
