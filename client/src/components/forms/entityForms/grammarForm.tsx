"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import NewElementButton from "@/components/buttons/newElementButton";
import AutoWidthInput from "@/components/input/autoWidthInput";
import AutoSizeTextArea from "@/components/textArea/autoSizeTextArea";
import { createGrammar, updateGrammar } from "@/api";
import MediaLoader from "@/components/mediaLoader";
import Grammar from "@/interface/features/Grammar";
import Passage from "@/interface/components/Passage";
import { faTrash, faAdd } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import UpdateButton from "@/components/buttons/updateButton";

export default function GrammarForm({grammar, unit_id}: {grammar?: Grammar; unit_id: string}) {
    const router = useRouter();
    const isUpdate = Boolean(grammar);

    let grammarData: Grammar;
    if (!grammar) {
        grammarData = {
            title: "",
            explanation: "",
            learnable_sentences: [],
            unit_id: unit_id
        };
    } else {
        grammarData = grammar;
    }
    
    const [title, setTitle] = useState<string>(grammarData.title);
    const [explanation, setExplanation] = useState<string>(grammarData.explanation);

    const [learnableSentence, setLearnableSentence] = useState<Passage[]>(grammarData.learnable_sentences!);

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
            unit_id: unit_id
        };
        
        try {
            if (isUpdate) {
                await updateGrammar(grammarData.id!, element);
            } else {
                await createGrammar(element);
            }

            router.push(`/languages/${languageId}/unit/${unit_id}`);
            router.refresh();
        } catch (error) {
            console.error(`Failed to ${isUpdate ? "update" : "create"} grammar:`, error);
            alert(`Failed to ${isUpdate ? "update" : "create"} grammar. Check console for details.`);
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
            <article className="flex flex-col space-y-2 items-center">
                <h3>Grammar Informations</h3>
                <AutoWidthInput
                    label="Title"
                    value={title}
                    onChange={(e) => setTitle(e.target.value)}
                    className="border border-gray-300"
                    required={true}
                />
                <AutoSizeTextArea
                    value={explanation}
                    onChange={(e) => setExplanation(e.target.value)}
                    label="Explanation"
                    required={true}
                />
            </article>
            <article className="flex flex-col space-y-2 items-center">
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
            </article>
            {isUpdate ? <UpdateButton>Update Grammar</UpdateButton> : <NewElementButton>Add Grammar</NewElementButton>}
        </form>
    );
}