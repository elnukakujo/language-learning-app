"use client";

import { useState } from "react";
import UpdateButton from "@/components/buttons/updateButton";
import ChangeUnitMenu from "@/components/selectMenu/changeUnitMenu";
import type Exercise from "@/interface/Exercise";

import ImageLoader from "@/components/imageLoader";
import AutoSizeTextArea from "@/components/textArea/autoSizeTextArea";
import OpenCloseMenu from "@/components/selectMenu/openCloseMenu";

interface UnitElements {
    vocabulary: {
        items: Array<{
            id: string;
            word: string;
            translation: string;
        }>;
        count: number;
    };
    grammar: {
        items: Array<{
            id: string;
            title: string;
        }>;
        count: number;
    };
    characters: {
        items: Array<{
            id: string;
            character: string;
            meaning: string;
        }>;
        count: number;
    };
}

export default function UpdateExerciseForm({ exercise, existingUnitsId, unitElements }: { exercise: Exercise, existingUnitsId: string[], unitElements: UnitElements }) {
    const [updatedQuestion, setUpdatedQuestion] = useState<string>(exercise.question);
    const [updatedAnswer, setUpdatedAnswer] = useState<string>(exercise.answer);

    const [updatedSupportText, setUpdatedSupportText] = useState<string>(exercise.support?.replace(/<image_url>.*?<\/image_url>/, '').trim() || "");
    const [updatedImageUrl, setUpdatedImageUrl] = useState<string | null>(exercise.support?.match(/<image_url>(.*?)<\/image_url>/)?.[1] || null);

    if (updatedImageUrl === "null") {
      setUpdatedImageUrl(null);
    }

    const [unitId, setUnitId] = useState<string>(exercise.unit_id);

    const [vocAssociated, setVocAssociated] = useState<string[]>(exercise.associated_to?.vocabulary || []);
    const [charAssociated, setCharAssociated] = useState<string[]>(exercise.associated_to?.characters || []);
    const [gramAssociated, setGramAssociated] = useState<string[]>(exercise.associated_to?.grammar || []);

    return (
      <form className="flex flex-col space-y-4 items-center">
        <ChangeUnitMenu unitsId={existingUnitsId} unitId={unitId} onChange={setUnitId} />
        <AutoSizeTextArea
          value={updatedQuestion}
          label="Question"
          onChange={(e) => setUpdatedQuestion(e.target.value)}
          placeholder="Enter question"
          className="border border-gray-300"
        />

        <AutoSizeTextArea
          value={updatedSupportText}
          label="Support"
          onChange={(e) => setUpdatedSupportText(e.target.value)}
          placeholder="Enter support text"
          className="border border-gray-300"
        />
        
        <ImageLoader
          previewUrl={updatedImageUrl}
          setPreviewUrl={(url) => {
            setUpdatedImageUrl(url);
          }}
        />

        <AutoSizeTextArea
          value={updatedAnswer}
          label="Answer"
          onChange={(e) => setUpdatedAnswer(e.target.value)}
          placeholder="Enter answer"
          className="border border-gray-300"
        />

        <section className="flex flex-col space-y-4 w-full items-baseline">
          <OpenCloseMenu
            elements={unitElements.vocabulary.items.map(item => ({id: item.id, value: item.word + " - " + item.translation}))}
            selectedElements={vocAssociated}
            setSelectedElements={setVocAssociated}
            label="Associated Vocabulary"
          />
          <OpenCloseMenu
            elements={unitElements.grammar.items.map(item => ({id: item.id, value: item.title}))}
            selectedElements={gramAssociated}
            setSelectedElements={setGramAssociated}
            label="Associated Grammar"
          />
          <OpenCloseMenu
            elements={unitElements.characters.items.map(item => ({id: item.id, value: item.character + " - " + item.meaning}))}
            selectedElements={charAssociated}
            setSelectedElements={setCharAssociated}
            label="Associated Characters"
          />
        </section>

        <UpdateButton
          element={{
              type_element: "ex",
              id: exercise.id,
              exercise_type: exercise.exercise_type,
              question: updatedQuestion,
              support: updatedSupportText + (updatedImageUrl ? `\n<image_url>${updatedImageUrl}</image_url>` : ''),
              answer: updatedAnswer,
              score: exercise.score,
              last_seen: exercise.last_seen,
              unit_id: unitId,
              associated_to: {
                vocabulary: vocAssociated,
                grammar: gramAssociated,
                characters: charAssociated
              }
          }}
        />
      </form>
    );
}