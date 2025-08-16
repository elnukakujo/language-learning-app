"use client";

import { useState } from "react";
import UpdateButton from "@/components/buttons/updateButton";
import ChangeUnitMenu from "@/components/selectMenu/changeUnitMenu";
import type Exercise from "@/interface/Exercise";

import ImageLoader from "@/components/imageLoader";
import AutoSizeTextArea from "@/components/textArea/autoSizeTextArea";

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

    const [isOpenVoc, setIsOpenVoc] = useState<boolean>(false);
    const [isOpenChar, setIsOpenChar] = useState<boolean>(false);
    const [isOpenGram, setIsOpenGram] = useState<boolean>(false);

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
          <label className="block text-sm font-medium text-gray-700">
            Associated Vocabulary
          </label>
          <button
            type="button"
            onClick={() => setIsOpenVoc(!isOpenVoc)}
            className="text-blue-600 button"
          >
            {isOpenVoc ? "Hide" : "Show"} Vocabulary
          </button>
          {isOpenVoc && (
            <ul className="max-w-[40rem] flex flex-row flex-wrap gap-2 mt-2">
              {unitElements.vocabulary.items.map((item) => (
                <li key={item.id}>
                  <button
                    type="button"
                    onClick={() => {
                      setVocAssociated((prev) => 
                        prev.includes(item.id) ? prev.filter(id => id !== item.id) : [...prev, item.id]
                      );
                    }}
                    className={`px-2 py-1 rounded-md ${
                      vocAssociated.includes(item.id) ? "bg-blue-600" : "bg-gray-700"
                    }`}
                  >
                    {item.word} - {item.translation}
                  </button>
                  
                </li>
              ))}
            </ul>
          )}
          <label className="block text-sm font-medium text-gray-700">
            Associated Grammar
          </label>
          <button
            type="button"
            onClick={() => setIsOpenGram(!isOpenGram)}
            className="text-blue-600 button"
          >
            {isOpenGram ? "Hide" : "Show"} Grammar
          </button>
          {isOpenGram && (
            <ul className="max-w-[40rem] flex flex-row flex-wrap gap-2 mt-2">
              {unitElements.grammar.items.map((item) => (
                <li key={item.id}>
                  <button
                    type="button"
                    onClick={() => {
                      setGramAssociated((prev) =>
                        prev.includes(item.id) ? prev.filter(id => id !== item.id) : [...prev, item.id]
                      );
                    }}
                    className={`px-2 py-1 rounded-md ${
                      gramAssociated.includes(item.id) ? "bg-blue-600" : "bg-gray-700"
                    }`}
                  >
                    {item.title}
                  </button>
                </li>
              ))}
            </ul>
          )}
          <label className="block text-sm font-medium text-gray-700">
            Associated Characters
          </label>
          <button
            type="button"
            onClick={() => setIsOpenChar(!isOpenChar)}
            className="text-blue-600 button"
          >
            {isOpenChar ? "Hide" : "Show"} Characters
          </button>
          {isOpenChar && (
            <ul className="max-w-[40rem] flex flex-row flex-wrap gap-2 mt-2">
              {unitElements.characters.items.map((item) => (
                <li key={item.id}>
                  <button
                    type="button"
                    onClick={() => {
                      setCharAssociated((prev) => 
                        prev.includes(item.id) ? prev.filter(id => id !== item.id) : [...prev, item.id]
                      );
                    }}
                    className={`px-2 py-1 rounded-md ${
                      charAssociated.includes(item.id) ? "bg-blue-600" : "bg-gray-700"
                    }`}
                  >
                    {item.character} - {item.meaning}
                  </button>
                  
                </li>
              ))}
            </ul>
          )}
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