"use client";
import { use, useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import NewElementButton from "@/components/buttons/newElementButton";
import AutoWidthInput from "@/components/input/autoWidthInput";
import ClassicSelectMenu from "@/components/selectMenu/classicSelectMenu";
import { createVocabulary } from "@/api";
import MediaLoader from "@/components/mediaLoader";
import Vocabulary from "@/interface/features/Vocabulary";
import Passage from "@/interface/components/Passage";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faAdd, faTrash } from "@fortawesome/free-solid-svg-icons";

export default function CreateVocabularyForm({ unit_id }: { unit_id: string }) {
    const router = useRouter();
    
    const [word, setWord] = useState<string>("");
    const [translation, setTranslation] = useState<string>("");
    const [phonetic, setPhonetic] = useState<string | undefined>(undefined);
    const [type, setType] = useState<'noun' | 'verb' | 'adjective' | 'adverb' | 'pronoun' | 'article' | 
        'preposition' | 'conjunction' | 'particle' | 'interjection' | 'numeral' | 
        'classifier' | 'auxiliary' | 'modal' | ''>("");
    const [gender, setGender] = useState<'m' | 'f' | 'n' | undefined>(undefined);
    const [wordImageUrl, setWordImageUrl] = useState<string[]>([]);
    const [wordAudioUrl, setWordAudioUrl] = useState<string[]>([]);

    const [exampleSentences, setExampleSentences] = useState<Passage[]>([]);

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
                image_files: wordImageUrl,
                audio_files: wordAudioUrl
            },
            example_sentences: exampleSentences,          
            unit_id: unit_id
        };
        console.log("Creating vocabulary with data:", element);
        
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
            className="flex flex-col space-y-12" 
            onSubmit={handleSubmit}
        >
            <article className="flex flex-col space-y-2 items-center">
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
                <ClassicSelectMenu
                    label="Gender of Word"
                    options={[
                        'm', 'f', 'n'
                    ]}
                    selectedOption={gender || ""}
                    onChange={(value) => setGender(value as typeof gender)}
                />
                <AutoWidthInput
                    value={phonetic || ""}
                    label="Phonetic"
                    onChange={(e) => setPhonetic(e.target.value)}
                    placeholder="Enter phonetic"
                    className="border border-gray-300"
                />
                <MediaLoader imageUrl={wordImageUrl} setImageUrl={setWordImageUrl} audioUrl={wordAudioUrl} setAudioUrl={setWordAudioUrl} />
            </article>
            <article className="flex flex-col space-y-2 items-center">
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
                            required
                            onChange={(e) => handleExampleSentenceChange(key, "text", e.target.value)}
                        />
                        <AutoWidthInput
                            label="Example Sentence Translation"
                            value={sentence.translation || ""}
                            className="border border-gray-300"
                            required
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
            </article>
            <NewElementButton>Add Vocabulary</NewElementButton>
        </form>
    );
}