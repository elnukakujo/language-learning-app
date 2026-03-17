"use client";

import { useState } from "react";
import UpdateButton from "@/components/buttons/updateButton";
import type Grammar from "@/interface/features/Grammar";
import AutoWidthInput from "@/components/input/autoWidthInput";
import AutoSizeTextArea from "@/components/textArea/autoSizeTextArea";
import { useRouter } from "next/navigation";
import { updateGrammar } from "@/api";
import MediaLoader from "@/components/mediaLoader";
import Passage from "@/interface/components/Passage";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faTrash, faAdd } from '@fortawesome/free-solid-svg-icons';

export default function updateGrammarForm({ grammar }: { grammar: Grammar }) {
  const router = useRouter();
  const [title, setTitle] = useState<string>(grammar.title);
  const [explanation, setExplanation] = useState<string>(grammar.explanation);

  const [learnableSentence, setLearnableSentence] = useState<Passage[]>(grammar.learnable_sentences || []);

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
      e.preventDefault();
      
      // Extract language_id from current URL
      const currentPath = window.location.pathname;
      const pathParts = currentPath.split('/');
      const languageId = pathParts[2]; // From /languages/LANG_ID/...
      
      const element: Grammar = {
        title: title,
        explanation: explanation,
        learnable_sentences: learnableSentence,
        unit_id: grammar.unit_id
      };
      
      try {
        await updateGrammar(grammar.id!, element);
        
        const router_path = `/languages/${languageId}/unit/${grammar.unit_id}/gram/${grammar.id}/`;
        
        router.push(router_path);
        router.refresh();
        
      } catch (error) {
        console.error("Failed to update grammar:", error);
        alert("Failed to update grammar. Check console for details.");
      }
    };
    const handleLearnableSentenceChange = (index: number, field: "text" | "translation" | "image_files" | "audio_files", value: string | string[]) => {
        setLearnableSentence(prevSentences => {
            const updatedSentences = [...prevSentences];
            const sentenceToUpdate = updatedSentences[index] || { text: "", translation: "", image_files: [], audio_files: [] };
            
            if (field === "text" || field === "translation") {
                sentenceToUpdate[field] = value as string;
            } else if (field === "image_files" || field === "audio_files") {
                sentenceToUpdate[field] = value as string[];
            }
            
            updatedSentences[index] = sentenceToUpdate;
            return updatedSentences;
        });
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
                <h3>Learnable Sentences</h3>
                {learnableSentence.map((sentence, key) => (
                    <section className="flex flex-col space-y-2 items-center" key={key}>
                        <button
                            className="h-fit px-2 py-1 bg-red-500 text-white rounded hover:bg-red-600 transition-colors"
                            onClick={() => {
                                setLearnableSentence(prev => prev.filter((_, index) => index !== key));
                            }}
                        >
                            <FontAwesomeIcon icon={faTrash}/>
                        </button>
                        <AutoWidthInput
                            label="Example Sentence"
                            value={sentence.text || ""}
                            className="border border-gray-300"
                            required={true}
                            onChange={(e) => handleLearnableSentenceChange(key, "text", e.target.value)}
                        />
                        <AutoWidthInput
                            label="Example Sentence Translation"
                            value={sentence.translation || ""}
                            className="border border-gray-300"
                            required={true}
                            onChange={(e) => handleLearnableSentenceChange(key, "translation", e.target.value)}
                        />
                        <MediaLoader imageUrl={sentence.image_files} setImageUrl={handleLearnableSentenceChange.bind(null, key, "image_files")} audioUrl={sentence.audio_files} setAudioUrl={handleLearnableSentenceChange.bind(null, key, "audio_files")} />
                </section>
                ))}
                <button
                    type="button"
                    onClick={() => {
                        setLearnableSentence(prev => [...prev, { text: "", translation: "", image_files: [], audio_files: [] }]);
                    }}
                    className="px-4 py-2 bg-blue-500 text-white rounded-md"
                >
                    <FontAwesomeIcon icon={faAdd}/>
                </button>
            </span>
            <UpdateButton>Update Grammar</UpdateButton>
        </form>
    );
}
