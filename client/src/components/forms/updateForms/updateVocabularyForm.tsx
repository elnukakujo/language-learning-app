"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";
import UpdateButton from "@/components/buttons/updateButton";
import type Vocabulary from "@/interface/features/Vocabulary";
import AutoWidthInput from "@/components/input/autoWidthInput";
import { updateVocabulary } from "@/api";
import ClassicSelectMenu from "@/components/selectMenu/classicSelectMenu";
import MediaLoader from "@/components/mediaLoader";
import { faAdd, faTrash } from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import Passage from "@/interface/components/Passage";

export default function updateVocabularyForm({ vocabulary }: { vocabulary: Vocabulary }) {
    const router = useRouter();

    const [word, setWord] = useState<string>(vocabulary.word.word);
    const [translation, setTranslation] = useState<string>(vocabulary.word.translation);
    const [phonetic, setPhonetic] = useState<string>(vocabulary.word.phonetic || "");
    const [type, setType] = useState<'noun' | 'verb' | 'adjective' | 'adverb' | 'pronoun' | 'article' | 
    'preposition' | 'conjunction' | 'particle' | 'interjection' | 'numeral' | 
    'classifier' | 'auxiliary' | 'modal' | ''>(vocabulary.word.type || "");
    const [gender, setGender] = useState<'m' | 'f' | 'n' | undefined>(vocabulary.word.gender);
    const [imageUrl, setImageUrl] = useState<string[]>(vocabulary.word.image_files || []);
    const [audioUrl, setAudioUrl] = useState<string[]>(vocabulary.word.audio_files || []);

    const [exampleSentences, setExampleSentences] = useState<Passage[]>(vocabulary.example_sentences || []);

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
                gender: gender,
                phonetic: phonetic,
                image_files: imageUrl,
                audio_files: audioUrl
            },
            example_sentences: exampleSentences,          
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

    const handleExampleSentenceChange = (index: number, field: "text" | "translation" | "image_files" | "audio_files", value: string | string[]) => {
        setExampleSentences(prevSentences => {
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
        <form 
            className="flex flex-col space-y-4" 
            onSubmit={handleSubmit}
        >
            <span className="flex flex-col space-y-2 items-center">
            <h3> Word Informations </h3>
            <AutoWidthInput
                value={word || ""}
                label="Word"
                onChange={(e) => setWord(e.target.value)}
                placeholder="Enter word"
                className="border border-gray-300"
                required={true}
            />
            <AutoWidthInput
                value={translation || ""}
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
                value={phonetic || ""}
                label="Phonetic"
                onChange={(e) => setPhonetic(e.target.value)}
                placeholder="Enter phonetic"
                className="border border-gray-300"
            />
            <ClassicSelectMenu
                label="Gender of Word"
                options={[
                'm', 'f', 'n'
                ]}
                selectedOption={gender || ""}
                onChange={(value) => setGender(value as typeof gender)}
            />
            <MediaLoader imageUrl={imageUrl} setImageUrl={setImageUrl} audioUrl={audioUrl} setAudioUrl={setAudioUrl} />
            </span>
            
            <span className="flex flex-col space-y-2 items-center">
                    <h3>Example Sentences</h3>
                    {exampleSentences.map((sentence, key) => (
                        <section className="flex flex-col space-y-2 items-center" key={key}>
                            <button
                                className="h-fit px-2 py-1 bg-red-500 text-white rounded hover:bg-red-600 transition-colors"
                                onClick={() => {
                                    setExampleSentences(prev => prev.filter((_, index) => index !== key));
                                }}
                            >
                                <FontAwesomeIcon icon={faTrash}/>
                            </button>
                            <AutoWidthInput
                                label="Example Sentence"
                                value={sentence.text || ""}
                                className="border border-gray-300"
                                required={true}
                                onChange={(e) => handleExampleSentenceChange(key, "text", e.target.value)}
                            />
                            <AutoWidthInput
                                label="Example Sentence Translation"
                                value={sentence.translation || ""}
                                className="border border-gray-300"
                                required={true}
                                onChange={(e) => handleExampleSentenceChange(key, "translation", e.target.value)}
                            />
                            <MediaLoader imageUrl={sentence.image_files} setImageUrl={handleExampleSentenceChange.bind(null, key, "image_files")} audioUrl={sentence.audio_files} setAudioUrl={handleExampleSentenceChange.bind(null, key, "audio_files")} />
                        </section>
                    ))}
                    <button
                        type="button"
                        onClick={() => {
                            setExampleSentences(prev => [...prev, { text: "", translation: "", image_files: [], audio_files: [] }]);
                        }}
                        className="px-4 py-2 bg-blue-500 text-white rounded-md"
                    >
                        <FontAwesomeIcon icon={faAdd}/>
                    </button>
                </span>
            <UpdateButton> Update Vocabulary</UpdateButton>
        </form>
    );
}
