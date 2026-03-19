"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import NewElementButton from "@/components/buttons/newElementButton";
import UpdateButton from "@/components/buttons/updateButton";
import ClassicSelectMenu from "@/components/selectMenu/classicSelectMenu";
import OpenCloseMenu from "@/components/selectMenu/openCloseMenu";
import AutoSizeTextArea from "@/components/textArea/autoSizeTextArea";
import TrueFalseInput from "@/components/input/trueFalseInput";
import DiscreteInput from "@/components/input/discreteInput";
import MediaLoader from "@/components/mediaLoader";
import { createExercise, updateExercise } from "@/api";
import ConversationInput from "@/components/input/conversationInput";
import type Calligraphy from "@/interface/features/Calligraphy";
import type Grammar from "@/interface/features/Grammar";
import type Vocabulary from "@/interface/features/Vocabulary";
import type Exercise from "@/interface/features/Exercise";

export interface UnitElements {
    vocabularies: Vocabulary[];
    grammars: Grammar[];
    calligraphies: Calligraphy[];
}

const EXERCISE_TYPE_OPTIONS: NonNullable<Exercise["exercise_type"]>[] = [
    "translate",
    "fill_in_the_blank",
    "essay",
    "true_false",
    "organize",
    "answering",
    "matching",
    "speaking",
    "conversation",
];

export default function ExerciseForm({
    exercise,
    unit_id,
    unitElements,
}: {
    exercise?: Exercise;
    unit_id: string;
    unitElements: UnitElements;
}) {
    const router = useRouter();
    const isUpdate = Boolean(exercise);

    let exerciseData: Exercise;
    if (!exercise) {
        exerciseData = {
            exercise_type: undefined,
            question: "",
            answer: "",
            text_support: "",
            image_files: [],
            audio_files: [],
            vocabulary_ids: [],
            grammar_ids: [],
            calligraphy_ids: [],
            unit_id,
        };
    } else {
        exerciseData = exercise;
    }

    const [exerciseType, setExerciseType] = useState<Exercise["exercise_type"]>(exerciseData.exercise_type);
    const [question, setQuestion] = useState<string>(exerciseData.question);
    const [answer, setAnswer] = useState<string>(exerciseData.answer);
    const [supportText, setSupportText] = useState<string>(exerciseData.text_support || "");

    const [imageUrl, setImageUrl] = useState<string[]>(exerciseData.image_files!);
    const [audioUrl, setAudioUrl] = useState<string[]>(exerciseData.audio_files!);

    const [vocAssociated, setVocAssociated] = useState<string[]>(exerciseData.vocabulary_ids!);
    const [callAssociated, setCallAssociated] = useState<string[]>(exerciseData.calligraphy_ids!);
    const [gramAssociated, setGramAssociated] = useState<string[]>(exerciseData.grammar_ids!);

    useEffect(() => {
        if (isUpdate) return;
        switch (exerciseType) {
            case "translate":
                setQuestion("A sentence to translate");
                setSupportText("");
                setAnswer("The translation");
                break;
            case "fill_in_the_blank":
                setQuestion("The house is __ and __.");
                setSupportText("");
                setAnswer("big__small");
                break;
            case "essay":
                setQuestion("Write here some requirements about the essay, and details");
                setSupportText("");
                setAnswer("Some helps and tips to write the essay");
                break;
            case "true_false":
                setQuestion("A statement to evaluate");
                setSupportText("");
                setAnswer("true");
                break;
            case "answering":
                setQuestion("A question to answer");
                setSupportText("");
                setAnswer("The answer to the question");
                break;
            case "speaking":
                setQuestion("A sentence to speak");
                setSupportText("");
                setAnswer("");
                break;
            default:
                setQuestion("");
                setSupportText("");
                setAnswer("");
                break;
        }
    }, [exerciseType, isUpdate]);

    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();

        const currentPath = window.location.pathname;
        const pathParts = currentPath.split("/");
        const languageId = pathParts[2];

        const element: Exercise = {
            exercise_type: exerciseType,
            question,
            text_support: supportText || undefined,
            image_files: imageUrl,
            audio_files: audioUrl,
            answer,
            unit_id,
            vocabulary_ids: vocAssociated,
            grammar_ids: gramAssociated,
            calligraphy_ids: callAssociated,
        };

        if (exerciseType === "speaking" && audioUrl.length === 0) {
            alert("Speaking exercises require an audio file. Please upload one.");
            return;
        }

        try {
            if (isUpdate) {
                await updateExercise(exerciseData.id!, element);
                router.push(`/languages/${languageId}/unit/${unit_id}/ex/${exerciseData.id}/`);
            } else {
                await createExercise(element);
                router.push(`/languages/${languageId}/unit/${unit_id}`);
            }

            router.refresh();
        } catch (error) {
            console.error(`Failed to ${isUpdate ? "update" : "create"} exercise:`, error);
            alert(`Failed to ${isUpdate ? "update" : "create"} exercise. Check console for details.`);
        }
    };

    return (
        <form className="flex flex-col space-y-4 items-center min-w-[40rem]" onSubmit={handleSubmit}>
            <ClassicSelectMenu
                label="Exercise Type"
                options={EXERCISE_TYPE_OPTIONS}
                selectedOption={exerciseType || ""}
                onChange={(value) => setExerciseType(value as Exercise["exercise_type"])}
                required
            />

            {exerciseType !== undefined && (
                <>
                    {!["matching", "organize", "conversation"].includes(exerciseType) && (
                        <AutoSizeTextArea
                            value={question}
                            onChange={(e) => setQuestion(e.target.value)}
                            className="flex w-full overflow-hidden border border-gray-300 rounded-md p-2"
                            label="Question"
                            required
                        />
                    )}

                    <AutoSizeTextArea
                        value={supportText}
                        onChange={(e) => setSupportText(e.target.value)}
                        className="flex w-full overflow-hidden border border-gray-300 rounded-md p-2"
                        label="Support"
                    />

                    <MediaLoader imageUrl={imageUrl} setImageUrl={setImageUrl} audioUrl={audioUrl} setAudioUrl={setAudioUrl} />

                    {exerciseType === "conversation" && (
                        <ConversationInput
                            value={question || undefined}   // question stores the full JSON
                            totalAudioSlots={audioUrl.length}
                            onChange={({ question: q, answer: a }) => {
                                setQuestion(q);
                                setAnswer(a);
                            }}
                        />
                    )}

                    {exerciseType === "true_false" && (
                        <TrueFalseInput
                            value={answer === "true"}
                            onChange={(e) => setAnswer(e.target.value)}
                            label="Answer"
                        />
                    )}

                    {["matching", "organize", "fill_in_the_blank"].includes(exerciseType) && (
                        <DiscreteInput
                            value={answer}
                            setValue={setAnswer}
                            label="Answer"
                            is2D={exerciseType === "matching"}
                        />
                    )}

                    {!["true_false", "matching", "organize", "speaking", "fill_in_the_blank", "conversation"].includes(exerciseType) && (
                        <AutoSizeTextArea
                            value={answer}
                            onChange={(e) => setAnswer(e.target.value)}
                            label="Answer"
                            required
                        />
                    )}

                    <section className="flex flex-col space-y-4 w-full items-baseline">
                        <OpenCloseMenu
                            elements={unitElements.vocabularies.map((item) => ({
                                id: item.id!,
                                value: item.word.word + " - " + item.word.translation,
                            }))}
                            selectedElements={vocAssociated}
                            setSelectedElements={setVocAssociated}
                            label="Associated Vocabulary"
                        />
                        <OpenCloseMenu
                            elements={unitElements.grammars.map((item) => ({ id: item.id!, value: item.title }))}
                            selectedElements={gramAssociated}
                            setSelectedElements={setGramAssociated}
                            label="Associated Grammar"
                        />
                        <OpenCloseMenu
                            elements={unitElements.calligraphies.map((item) => ({
                                id: item.id!,
                                value: item.character.character + " - " + item.character.phonetic,
                            }))}
                            selectedElements={callAssociated}
                            setSelectedElements={setCallAssociated}
                            label="Associated Calligraphies"
                        />
                    </section>

                    {isUpdate ? <UpdateButton>Update Exercise</UpdateButton> : <NewElementButton>Add Exercise</NewElementButton>}
                </>
            )}
        </form>
    );
}