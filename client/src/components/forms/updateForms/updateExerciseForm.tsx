"use client";

import { useState, useRef, useEffect } from "react";
import UpdateButton from "@/components/buttons/updateButton";
import ChangeUnitMenu from "@/components/selectMenu/changeUnitMenu";
import type Exercise from "@/interface/Exercise";

import ImageLoader from "@/components/imageLoader";

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
    const [question, setQuestion] = useState<string>(exercise.question);
    const [answer, setAnswer] = useState<string>(exercise.answer);

    const [supportText, setSupportText] = useState<string>(exercise.support?.replace(/<image_url>.*?<\/image_url>/, '').trim() || "");
    const [imageUrl, setImageUrl] = useState<string | null>(exercise.support?.match(/<image_url>(.*?)<\/image_url>/)?.[1] || null);
    
    if (imageUrl === "null") {
      setImageUrl(null);
    }

    const [unitId, setUnitId] = useState<string>(exercise.unit_id);

    const [vocAssociated, setVocAssociated] = useState<string[]>(exercise.associated_to?.vocabulary || []);
    const [charAssociated, setCharAssociated] = useState<string[]>(exercise.associated_to?.characters || []);
    const [gramAssociated, setGramAssociated] = useState<string[]>(exercise.associated_to?.grammar || []);

    const [isOpenVoc, setIsOpenVoc] = useState<boolean>(false);
    const [isOpenChar, setIsOpenChar] = useState<boolean>(false);
    const [isOpenGram, setIsOpenGram] = useState<boolean>(false);

    const questionRef = useRef<HTMLTextAreaElement>(null);
    const supportRef = useRef<HTMLTextAreaElement>(null);
    const answerRef = useRef<HTMLTextAreaElement>(null);

    function useAutoResize(
          ref: React.RefObject<HTMLTextAreaElement | null>,
          value: string
        ) {
      useEffect(() => {
      const textarea = ref.current;
      if (textarea) {
        textarea.style.height = "auto";
        textarea.style.height = `${textarea.scrollHeight}px`;
      }
      }, [value, ref]);
    }

    useAutoResize(questionRef, question);
    useAutoResize(supportRef, supportText);
    useAutoResize(answerRef, answer);

    return (
      <form className="flex flex-col space-y-4">
        <section className="flex flex-col space-y-2 h-fit">
          <ChangeUnitMenu unitsId={existingUnitsId} unitId={unitId} onChange={setUnitId} />
          <article>
            <label htmlFor="">
              Question
            </label>
            <textarea
                ref={questionRef}
                value={question}
                onChange={(e) => {
                    const newValue = e.target.value;
                    setQuestion(newValue);
                }}
                className="flex w-full overflow-hidden border border-gray-300 rounded-md p-2"
            />
          </article>
          <article>
            <label htmlFor="">
              Support
            </label>
            <textarea
                ref={supportRef}
                value={supportText}
                onChange={(e) => {
                    const newValue = e.target.value;
                    setSupportText(newValue);
                }}
                className="flex w-full overflow-hidden border border-gray-300 rounded-md p-2"
            />
            <ImageLoader
              previewUrl={imageUrl}
              setPreviewUrl={(url) => {
                setImageUrl(url);
              }}
            />
          </article>
          <article>
            <label htmlFor="">
              Answer
            </label>
            <textarea
                ref={answerRef}
                value={answer}
                onChange={(e) => {
                    const newValue = e.target.value;
                    setAnswer(newValue);
                }}
                className="flex w-full overflow-hidden border border-gray-300 rounded-md p-2"
            />
          </article>
        </section>
        <section>
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
              question: question,
              support: supportText + (imageUrl ? `\n<image_url>${imageUrl}</image_url>` : ''),
              answer: answer,
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