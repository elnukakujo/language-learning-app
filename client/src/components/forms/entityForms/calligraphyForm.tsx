"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";
import NewElementButton from "@/components/buttons/newElementButton";
import AutoWidthInput from "@/components/input/autoWidthInput";
import TagSelector from "@/components/selectMenu/tagSelector";
import SourceSelector from "@/components/selectMenu/sourceSelector";
import { createCalligraphy, updateCalligraphy } from "@/api/calligraphy";
import MediaLoader from "@/components/mediaLoader";
import Calligraphy from "@/interface/features/Calligraphy";
import ClassicSelectMenu from "@/components/selectMenu/classicSelectMenu";
import Word from "@/interface/components/Word";
import Passage from "@/interface/components/Passage";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faTrash, faAdd } from "@fortawesome/free-solid-svg-icons";
import UpdateButton from "@/components/buttons/updateButton";
import ConflictError from "@/api/conflictError";
import ConflictDialog from "@/components/dialogs/conflictDialog";

export default function CalligraphyForm({calligraphy, lesson_id}: {calligraphy?: Partial<Calligraphy>; lesson_id: string}) {
    const router = useRouter();
    const isUpdate = Boolean(calligraphy?.id);
    let calligraphyData: Partial<Calligraphy>;
    if (!calligraphy) {
        calligraphyData = {
            character: {
                character: "",
                phonetic: "",
                meaning: "",
                radical: "",
                strokes: 0,
                image_files: [],
                audio_files: []
            },
            example_words: [],
            example_sentences: [],
            lesson_id: lesson_id
        };
    } else {
        calligraphyData = calligraphy;
    }
    
    const [character, setCharacter] = useState<string>(calligraphyData.character?.character || "");
    const [phonetic, setPhonetic] = useState<string>(calligraphyData.character?.phonetic || "");
    const [meaning, setMeaning] = useState<string|undefined>(calligraphyData.character?.meaning || undefined);
    const [radical, setRadical] = useState<string|undefined>(calligraphyData.character?.radical || undefined);
    const [strokes, setStrokes] = useState<number|undefined>(calligraphyData.character?.strokes || undefined);
    const [imageUrl, setImageUrl] = useState<string[]>(calligraphyData.character?.image_files || []);
    const [audioUrl, setAudioUrl] = useState<string[]>(calligraphyData.character?.audio_files || []);

    const [exampleWords, setExampleWords] = useState<Partial<Word>[]>(calligraphyData.example_words ? calligraphyData.example_words : []);
    const [exampleSentences, setExampleSentences] = useState<Partial<Passage>[]>(calligraphyData.example_sentences ? calligraphyData.example_sentences : []);
    const [selectedTagIds, setSelectedTagIds] = useState<string[]>(calligraphyData.tags ? calligraphyData.tags.map(tag => tag.id!) : []);
    const [selectedSourceIds, setSelectedSourceIds] = useState<string[]>(calligraphyData.sources ? calligraphyData.sources.map(source => source.id!) : []);
    const [conflict, setConflict] = useState<ConflictError | null>(null);

    const buildElement = (): Partial<Calligraphy> => ({
        character: {
            character: character,
            phonetic: phonetic,
            meaning: meaning,
            radical: radical,
            strokes: strokes,
            image_files: imageUrl,
            audio_files: audioUrl
        },
        example_words: exampleWords,
        example_sentences: exampleSentences,
        lesson_id: lesson_id,
        tags: selectedTagIds.map(id => ({ id })),
        sources: selectedSourceIds.map(id => ({ id }))
    });

    // Extract language_id from current URL
    const languageIdFromPath = () => window.location.pathname.split('/')[2]; // From /languages/LANG_ID/...

    const submit = async (element: Partial<Calligraphy>, onConflict?: "keep" | "overwrite" | "merge") => {
        if (isUpdate) {
            await updateCalligraphy(calligraphyData.id!, element);
        } else {
            await createCalligraphy(element, onConflict);
        }
        router.push(`/languages/${languageIdFromPath()}/lesson/${lesson_id}`);
        router.refresh();
    };

    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        const element = buildElement();

        try {
            await submit(element);
        } catch (error) {
            if (error instanceof ConflictError) {
                setConflict(error);
                return;
            }
            console.error(`Failed to ${isUpdate ? "update" : "create"} calligraphy:`, error);
            alert(`Failed to ${isUpdate ? "update" : "create"} calligraphy. Check console for details.`);
        }
    };

    const resolveConflict = async (element: Partial<Calligraphy>, onConflict: "keep" | "overwrite" | "merge") => {
        setConflict(null);
        try {
            await submit(element, onConflict);
        } catch (error) {
            console.error("Failed to resolve calligraphy conflict:", error);
            alert("Failed to resolve conflict. Check console for details.");
        }
    };

    const handleKeepExisting = () => resolveConflict(buildElement(), "keep");
    const handleOverwrite = () => resolveConflict(buildElement(), "overwrite");
    const handleManualResolve = (resolvedFields: Record<string, string>) => {
        const element = buildElement();
        Object.assign(element.character!, resolvedFields);
        resolveConflict(element, "merge");
    };
    const handleExampleWordChange = (index: number, field: "word" | "translation" | "word_type" | "word_gender" | "image_files" | "audio_files", value: string | string[]) => {
        setExampleWords(prevWords => {
            const updatedWords = [...prevWords];
            const wordToUpdate = updatedWords[index] || { word: "", translation: "", word_type: "" as const, image_files: [], audio_files: [] };
            
            if (field === "word" || field === "translation" || field === "word_type" || field === "word_gender") {
                (wordToUpdate as { [key: string]: string | string[] })[field] = value as string;
            } else if (field === "image_files" || field === "audio_files") {
                (wordToUpdate as { [key: string]: string | string[] })[field] = value as string[];
            }
            
            updatedWords[index] = wordToUpdate;
            return updatedWords;
        });
    };

    const handleExampleSentenceChange = (index: number, field: "text" | "translation" | "image_files" | "audio_files", value: string | string[]) => {
        setExampleSentences(prevSentences => {
            const updatedSentences = [...prevSentences];
            const sentenceToUpdate = updatedSentences[index] || { text: "", translation: "", image_files: [], audio_files: [] };
            
            if (field === "text" || field === "translation") {
                (sentenceToUpdate as { [key: string]: string | string[] })[field] = value as string;
            } else if (field === "image_files" || field === "audio_files") {
                (sentenceToUpdate as { [key: string]: string | string[] })[field] = value as string[];
            }
            
            updatedSentences[index] = sentenceToUpdate;
            return updatedSentences;
        });
    };

    return (
        <>
        {conflict && (
            <ConflictDialog
                error={conflict}
                onKeep={handleKeepExisting}
                onOverwrite={handleOverwrite}
                onManualResolve={handleManualResolve}
                onCancel={() => setConflict(null)}
            />
        )}
        <form className="flex flex-col space-y-12" onSubmit={handleSubmit}>
            <article className="flex flex-col space-y-2 items-center">
                <h3>Character Informations</h3>
                <AutoWidthInput
                    value={character}
                    onChange={(e) => setCharacter(e.target.value)}
                    label="Character"
                    className="border border-gray-300"
                    required
                />
                <AutoWidthInput
                    value={phonetic}
                    onChange={(e) => setPhonetic(e.target.value)}
                    label="Phonetic"
                    className="border border-gray-300"
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
            <TagSelector
                selectedTagIds={selectedTagIds}
                onTagsChange={setSelectedTagIds}
                elementId={calligraphyData.id!}
            />
            <SourceSelector
                selectedSourceIds={selectedSourceIds}
                onSourcesChange={setSelectedSourceIds}
                elementId={calligraphyData.id!}
            />
            <article className="flex flex-col space-y-2 items-center">
                <h3>Example Words</h3>
                {exampleWords.map((exampleWord, key) => (
                    <section key={key} className="flex flex-col space-y-2 items-center w-full border border-gray-300 p-4 rounded">
                        <button
                            type="button"
                            className="h-fit px-2 py-1 bg-red-500 text-white rounded hover:bg-red-600 transition-colors"
                            onClick={() => {
                                setExampleWords(prev => prev.filter((_, index) => index !== key));
                            }}
                        >
                            <FontAwesomeIcon icon={faTrash}/>
                        </button>
                        <AutoWidthInput
                            value={exampleWord.word || ""}
                            onChange={(e) => handleExampleWordChange(key, "word", e.target.value)}
                            label="Example Word"
                            className="border border-gray-300"
                            required
                        />
                        <AutoWidthInput
                            value={exampleWord.translation || ""}
                            onChange={(e) => handleExampleWordChange(key, "translation", e.target.value)}
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
                            selectedOption={exampleWord.word_type || ""}
                            onChange={(value) => handleExampleWordChange(key, "word_type", value)}
                        />
                        <ClassicSelectMenu
                            label="Gender of Word"
                            options={[
                                'm', 'f', 'n', 'c', ''
                            ]}
                            selectedOption={exampleWord.word_gender || ""}
                            onChange={(value) => handleExampleWordChange(key, "word_gender", value)}
                        />
                        <MediaLoader 
                            imageUrl={exampleWord.image_files || []} 
                            setImageUrl={(files) => handleExampleWordChange(key, "image_files", files)} 
                            audioUrl={exampleWord.audio_files || []} 
                            setAudioUrl={(files) => handleExampleWordChange(key, "audio_files", files)}
                        />
                    </section>
                ))}
                <button
                    type="button"
                    onClick={() => {
                        setExampleWords(prev => [...prev, { word: "", translation: "", word_type: "noun", image_files: [], audio_files: [] }]);
                    }}
                    className="px-4 py-2 bg-blue-500 text-white rounded-md"
                >
                    <FontAwesomeIcon icon={faAdd}/> Add Example Word
                </button>
            </article>
            <article className="flex flex-col space-y-2 items-center">
                <h3>Example Sentences</h3>
                {exampleSentences.map((exampleSentence, key) => (
                    <section key={key} className="flex flex-col space-y-2 items-center w-full border border-gray-300 p-4 rounded">
                        <button
                            type="button"
                            className="h-fit px-2 py-1 bg-red-500 text-white rounded hover:bg-red-600 transition-colors"
                            onClick={() => {
                                setExampleSentences(prev => prev.filter((_, index) => index !== key));
                            }}
                        >
                            <FontAwesomeIcon icon={faTrash}/>
                        </button>
                        <AutoWidthInput
                            value={exampleSentence.text || ""}
                            onChange={(e) => handleExampleSentenceChange(key, "text", e.target.value)}
                            label="Example Sentence"
                            className="border border-gray-300"
                            required
                        />
                        <AutoWidthInput
                            value={exampleSentence.translation || ""}
                            onChange={(e) => handleExampleSentenceChange(key, "translation", e.target.value)}
                            label="Example Sentence Translation"
                            className="border border-gray-300"
                        />
                        <MediaLoader 
                            imageUrl={exampleSentence.image_files || []} 
                            setImageUrl={(files) => handleExampleSentenceChange(key, "image_files", files)} 
                            audioUrl={exampleSentence.audio_files || []} 
                            setAudioUrl={(files) => handleExampleSentenceChange(key, "audio_files", files)}
                        />
                    </section>
                ))}
                <button
                    type="button"
                    onClick={() => {
                        setExampleSentences(prev => [...prev, { text: "", translation: "", image_files: [], audio_files: [] }]);
                    }}
                    className="px-4 py-2 bg-blue-500 text-white rounded-md"
                >
                    <FontAwesomeIcon icon={faAdd}/> Add Example Sentence
                </button>
            </article>
            {isUpdate ? <UpdateButton>Update Calligraphy</UpdateButton> : <NewElementButton>Add Calligraphy</NewElementButton>}
        </form>
        </>
    );
}