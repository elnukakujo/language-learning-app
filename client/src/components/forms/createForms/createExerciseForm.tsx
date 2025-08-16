"use client";

import { useState, useEffect } from "react";
import NewElementButton from "@/components/buttons/newElementButton";
import ClassicSelectMenu from "@/components/selectMenu/classicSelectMenu";
import ImageLoader from "@/components/imageLoader";
import AutoSizeTextArea from "@/components/textArea/autoSizeTextArea";
import TrueFalseInput from "@/components/input/trueFalseInput";

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

export default function CreateExerciseForm({ unit_id, unitElements }: { unit_id: string, unitElements: UnitElements }) {
    const [exerciseType, setExerciseType] = useState<string>("")
    const [question, setQuestion] = useState<string>("")
    const [answer, setAnswer] = useState<string>("")
    const [supportText, setSupportText] = useState<string>("")
    const [imageUrl, setImageUrl] = useState<string | null>(null);

    const [vocAssociated, setVocAssociated] = useState<string[]>([]);
    const [charAssociated, setCharAssociated] = useState<string[]>([]);
    const [gramAssociated, setGramAssociated] = useState<string[]>([]);

    const [isOpenVoc, setIsOpenVoc] = useState<boolean>(false);
    const [isOpenChar, setIsOpenChar] = useState<boolean>(false);
    const [isOpenGram, setIsOpenGram] = useState<boolean>(false);

    useEffect(() => {
      switch (exerciseType) {
        case "translate":
          setQuestion("-- A sentence to translate --");
          setSupportText("");
          setAnswer("-- The translation --");
          break;
        case "fill-in-the-blank":
          setQuestion("-- The house is __ and __. --");
          setSupportText("");
          setAnswer("-- big__small --");
          break;
        case "essay":
          setQuestion("-- Write here some requirements about the essay, and details --");
          setSupportText("");
          setAnswer("-- Some helps and tips to write the essay --");
          break;
        case "true-false":
          setQuestion("-- A statement to evaluate --");
          setSupportText("");
          setAnswer("true");
          break;
        case "organize":
          setQuestion("-- My/house/small/purple/and/is --");
          setSupportText("");
          setAnswer("-- My house is small and purple --");
          break;
        case "answering":
          setQuestion("-- A question to answer --");
          setSupportText("");
          setAnswer("-- The answer to the question --");
          break;
        default:
          setQuestion("");
          setSupportText("");
          setAnswer("");
          break;
      }
    }, [exerciseType]); 

    return (
      <form className="flex flex-col space-y-4 items-center min-w-[40rem]">
        <ClassicSelectMenu
          options={[
            "translate",
            "fill-in-the-blank",
            "essay",
            "true-false",
            "organize",
            "answering",
          ]}
          selectedOption={exerciseType}
          onChange={setExerciseType}
        />
        {exerciseType !== "" && (
          <>
            <AutoSizeTextArea
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              className="flex w-full overflow-hidden border border-gray-300 rounded-md p-2"
              label="Question"
            />
            <AutoSizeTextArea
              value={supportText}
              onChange={(e) => setSupportText(e.target.value)}
              className="flex w-full overflow-hidden border border-gray-300 rounded-md p-2"
              label="Support"
            />
            <ImageLoader previewUrl={imageUrl} setPreviewUrl={setImageUrl} />

            {exerciseType === "true-false" ? (
              <TrueFalseInput
                value={answer === "true"}
                onChange={(e) => setAnswer(e.target.value)}
                label="Answer"
              />
            ) : 
              <AutoSizeTextArea
                value={answer}
                onChange={(e) => setAnswer(e.target.value)}
                label="Answer"
              />
            }
            
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
            <NewElementButton
              element={{
                  type_element: "ex",
                  id: "",
                  exercise_type: exerciseType,
                  question: question,
                  support: supportText + (imageUrl ? "\n<image_url>"+imageUrl+"</image_url>" : ""),
                  answer: answer,
                  score: 0.0,
                  last_seen: new Date,
                  unit_id: unit_id,
                  associated_to: {
                    vocabulary: vocAssociated,
                    grammar: gramAssociated,
                    characters: charAssociated
                  }
            }}
            />
          </>
        )}
      </form>
    );
}