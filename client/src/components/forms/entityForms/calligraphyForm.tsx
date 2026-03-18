"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";
import NewElementButton from "@/components/buttons/newElementButton";
import AutoWidthInput from "@/components/input/autoWidthInput";
import { createCalligraphy, updateCalligraphy } from "@/api";
import MediaLoader from "@/components/mediaLoader";
import Calligraphy from "@/interface/features/Calligraphy";
import ClassicSelectMenu from "@/components/selectMenu/classicSelectMenu";
import Word from "@/interface/components/Word";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faTrash, faAdd } from "@fortawesome/free-solid-svg-icons";
import UpdateButton from "@/components/buttons/updateButton";

export default function CalligraphyForm({calligraphy, unit_id}: {calligraphy?: Calligraphy; unit_id: string}) {
    const router = useRouter();
    const isUpdate = Boolean(calligraphy);
    let calligraphyData: Calligraphy;
    if (!calligraphy) {
        calligraphyData = {
            character: {
                character: "",
                phonetic: "",
                meaning: "",
                radical: "",
                strokes: undefined,
                image_files: [],
                audio_files: []
            },
            example_word: undefined,
            unit_id: unit_id
        };
    } else {
        calligraphyData = calligraphy;
    }
    
    const [character, setCharacter] = useState<string>(calligraphyData.character.character);
    const [phonetic, setPhonetic] = useState<string>(calligraphyData.character.phonetic);
    const [meaning, setMeaning] = useState<string|undefined>(calligraphyData.character.meaning);
    const [radical, setRadical] = useState<string|undefined>(calligraphyData.character.radical);
    const [strokes, setStrokes] = useState<number|undefined>(calligraphyData.character.strokes);
    const [imageUrl, setImageUrl] = useState<string[]>(calligraphyData.character.image_files!);
    const [audioUrl, setAudioUrl] = useState<string[]>(calligraphyData.character.audio_files!);

    const [exampleWord, setExampleWord] = useState<Word | undefined>(undefined);

    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        
        // Extract language_id from current URL
        const currentPath = window.location.pathname;
        const pathParts = currentPath.split('/');
        const languageId = pathParts[2]; // From /languages/LANG_ID/...
        
        const element: Calligraphy = {
            character: {
                character: character,
                phonetic: phonetic,
                meaning: meaning,
                radical: radical,
                strokes: strokes,
                image_files: imageUrl,
                audio_files: audioUrl
            },
            example_word: exampleWord,
            unit_id: unit_id
        };
        
        try {
            if (isUpdate) {
                await updateCalligraphy(calligraphyData.id!, element);
            } else {
                await createCalligraphy(element);
            }

            router.push(`/languages/${languageId}/unit/${unit_id}`);
            router.refresh();
        } catch (error) {
            console.error(`Failed to ${isUpdate ? "update" : "create"} calligraphy:`, error);
            alert(`Failed to ${isUpdate ? "update" : "create"} calligraphy. Check console for details.`);
        }
    };
    const handleExampleWordChange = (field: "word" | "translation" | "type" | "gender" | "image_files" | "audio_files", value: string | string[]) => {
        setExampleWord(prevWord => {
            if (!prevWord) return prevWord;
                const updatedWord = { ...prevWord };
            if (["word", "translation", "type", "gender"].includes(field)) {
                (updatedWord as { [key: string]: string | string[] })[field] = value as string;
            } else if (["image_files", "audio_files"].includes(field)) {
                (updatedWord as { [key: string]: string | string[] })[field] = value as string[];
            }
            return updatedWord;
        });
    };

    return (
        <form className="flex flex-col space-y-12" onSubmit={handleSubmit}>
            <article className="flex flex-col space-y-2 items-center">
                <h3>Character Informations</h3>
                <AutoWidthInput
                    value={character}
                    onChange={(e) => setCharacter(e.target.value)}
                    label="Character"
                    className="border border-gray-300"
                    required={true}
                />
                <AutoWidthInput
                    value={phonetic}
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
                    value={radical || ""}
                    onChange={(e) => setRadical(e.target.value)}
                    label="Radical"
                    className="border border-gray-300"
                />
                <AutoWidthInput
                    value={strokes !== undefined ? strokes.toString() : ""}
                    onChange={(e) => setStrokes(parseInt(e.target.value) || undefined)}
                    label="Strokes"
                    className="border border-gray-300"
                />
                <MediaLoader imageUrl={imageUrl} setImageUrl={setImageUrl} audioUrl={audioUrl} setAudioUrl={setAudioUrl} />
            </article>
            <article className="flex flex-col space-y-2 items-center">
                <h3>Example Word Informations</h3>
                {exampleWord && (<section className="flex flex-col space-y-2 items-center">
                    <button
                        className="h-fit px-2 py-1 bg-red-500 text-white rounded hover:bg-red-600 transition-colors"
                        onClick={() => {
                            setExampleWord(undefined);
                        }}
                    >
                        <FontAwesomeIcon icon={faTrash}/>
                    </button>
                    <AutoWidthInput
                        value={exampleWord.word}
                        onChange={(e) => handleExampleWordChange("word", e.target.value)}
                        label="Example Word"
                        className="border border-gray-300"
                        required
                    />
                    <AutoWidthInput
                        value={exampleWord.translation}
                        onChange={(e) => handleExampleWordChange("translation", e.target.value)}
                        label="Example Word Translation"
                        className="border border-gray-300"
                        required
                    />
                    <ClassicSelectMenu
                        label="Type of Word"
                        options={[
                            'noun', 'verb', 'adjective', 'adverb', 'pronoun', 'article', 
                            'preposition', 'conjunction', 'particle', 'interjection', 'numeral', 
                            'classifier', 'auxiliary', 'modal'
                        ]}
                        selectedOption={exampleWord.type}
                        onChange={(value) => handleExampleWordChange("type", value)}
                        required
                    />
                    <ClassicSelectMenu
                        label="Gender of Word"
                        options={[
                            'm', 'f', 'n'
                        ]}
                        selectedOption={exampleWord.gender || ""}
                        onChange={(value) => handleExampleWordChange("gender", value)}
                    />
                    <MediaLoader 
                        imageUrl={exampleWord.image_files} 
                        setImageUrl={handleExampleWordChange.bind(null, "image_files")} 
                        audioUrl={exampleWord.audio_files} 
                        setAudioUrl={handleExampleWordChange.bind(null, "audio_files")}
                    />
                </section>)}
                {!exampleWord && (
                    <button
                        type="button"
                        onClick={() => {
                            setExampleWord({ word: "", translation: "", type: "" as Word["type"], image_files: [], audio_files: [] });
                        }}
                        className="px-4 py-2 bg-blue-500 text-white rounded-md"
                    >
                        <FontAwesomeIcon icon={faAdd}/>
                    </button>
                )}
            </article>
            {isUpdate ? <UpdateButton>Update Calligraphy</UpdateButton> : <NewElementButton>Add Calligraphy</NewElementButton>}
        </form>
    );
}