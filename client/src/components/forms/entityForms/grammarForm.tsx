"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import NewElementButton from "@/components/buttons/newElementButton";
import AutoWidthInput from "@/components/input/autoWidthInput";
import AutoSizeTextArea from "@/components/textArea/autoSizeTextArea";
import TagSelector from "@/components/selectMenu/tagSelector";
import SourceSelector from "@/components/selectMenu/sourceSelector";
import { createGrammar, updateGrammar } from "@/api/grammar";
import MediaLoader from "@/components/mediaLoader";
import Grammar from "@/interface/features/Grammar";
import Passage from "@/interface/components/Passage";
import { faTrash, faAdd } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import UpdateButton from "@/components/buttons/updateButton";

export default function GrammarForm({grammar, lesson_id}: {grammar?: Partial<Grammar>; lesson_id: string}) {
    const router = useRouter();
    const isUpdate = Boolean(grammar?.id);

    let grammarData: Partial<Grammar>;
    if (!grammar) {
        grammarData = {
            title: "",
            explanation: "",
            example_sentences: [],
            lesson_id: lesson_id
        };
    } else {
        grammarData = grammar;
    }
    
    const [title, setTitle] = useState<string>(grammarData.title || "");
    const [explanation, setExplanation] = useState<string>(grammarData.explanation || "");

    const [learnableSentence, setLearnableSentence] = useState<Partial<Passage>[]>(grammarData.example_sentences!);
    const [selectedTagIds, setSelectedTagIds] = useState<string[]>(grammarData.tags ? grammarData.tags.map(tag => tag.id!) : []);
    const [selectedSourceIds, setSelectedSourceIds] = useState<string[]>(grammarData.sources ? grammarData.sources.map(source => source.id!) : []);

    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        
        // Extract language_id from current URL
        const currentPath = window.location.pathname;
        const pathParts = currentPath.split('/');
        const languageId = pathParts[2]; // From /languages/LANG_ID/...
        
        const element: Partial<Grammar> = {
            title: title,
            explanation: explanation,
            example_sentences: learnableSentence,
            lesson_id: lesson_id,
            tags: selectedTagIds.map(id => ({ id })),
            sources: selectedSourceIds.map(id => ({ id }))
        };
        
        try {
            let grammarId: string;
            if (isUpdate) {
                await updateGrammar(grammarData.id!, element);
                grammarId = grammarData.id!;
            } else {
                const response = await createGrammar(element);
                grammarId = response.id;
            }

            router.push(`/languages/${languageId}/lesson/${lesson_id}`);
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
            <TagSelector
                selectedTagIds={selectedTagIds}
                onTagsChange={setSelectedTagIds}
                elementId={grammarData.id!}
            />
            <SourceSelector
                selectedSourceIds={selectedSourceIds}
                onSourcesChange={setSelectedSourceIds}
                elementId={grammarData.id!}
            />
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