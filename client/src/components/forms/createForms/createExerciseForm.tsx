"use client";

import { useState, useEffect, useRef } from "react";
import NewElementButton from "@/components/buttons/newElementButton";
import ClassicSelectMenu from "@/components/selectMenu/classicSelectMenu";
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

export default function CreateExerciseForm({ unit_id, unitElements }: { unit_id: string, unitElements: UnitElements }) {
    const [exerciseType, setExerciseType] = useState<string>("")
    const [support, setSupport] = useState<string>("")
    const [question, setQuestion] = useState<string>("")
    const [answer, setAnswer] = useState<string>("")
    const [imageUrl, setImageUrl] = useState<string | null>(null);

    const [vocAssociated, setVocAssociated] = useState<string[]>([]);
    const [charAssociated, setCharAssociated] = useState<string[]>([]);
    const [gramAssociated, setGramAssociated] = useState<string[]>([]);

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
    useAutoResize(supportRef, support);
    useAutoResize(answerRef, answer);

    useEffect(() => {
      switch (exerciseType) {
        case "translate":
          setQuestion("-- A sentence to translate --");
          setSupport("");
          setAnswer("-- The translation --");
          break;
        case "fill-in-the-blank":
          setQuestion("-- The house is __ and __. --");
          setSupport("");
          setAnswer("-- big__small --");
          break;
        case "essay":
          setQuestion("-- Write here some requirements about the essay, and details --");
          setSupport("");
          setAnswer("-- Some helps and tips to write the essay --");
          break;
        case "true-false":
          setQuestion("-- A statement to evaluate --");
          setSupport("");
          setAnswer("true");
          break;
        case "organize":
          setQuestion("-- My/house/small/purple/and/is --");
          setSupport("");
          setAnswer("-- My house is small and purple --");
          break;
        case "answering":
          setQuestion("-- A question to answer --");
          setSupport("");
          setAnswer("-- The answer to the question --");
          break;
        default:
          setQuestion("");
          setSupport("");
          setAnswer("");
          break;
      }
    }, [exerciseType]); 

    return (
      <form className="flex flex-col space-y-4 min-w-[40rem]">
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
            <section>
              <label htmlFor="question" className="block text-sm font-medium text-gray-700">
                Question
              </label>
              <textarea
                ref={questionRef}
                id="question"
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                className="flex w-full overflow-hidden border border-gray-300 rounded-md p-2"
                required
              />
            </section>
            <section>
              <label htmlFor="support" className="block text-sm font-medium text-gray-700">
                Support
              </label>
              <textarea
                ref={supportRef}
                id="support"
                value={support}
                onChange={(e) => setSupport(e.target.value)}
                className="flex w-full overflow-hidden border border-gray-300 rounded-md p-2"
                required
              />
              <ImageLoader previewUrl={imageUrl} setPreviewUrl={setImageUrl} />
            </section>
            <section>
              <label htmlFor="answer" className="block text-sm font-medium text-gray-700">
                Answer
              </label>
              {exerciseType === "true-false" ? (
                <div className="flex flex-row space-x-2">
                  <span className="flex items-center space-x-2">
                    <input
                      id="answer-true"
                      type="radio"
                      checked={answer === "true"}
                      onChange={() => setAnswer("true")}
                      className="h-4 w-4 text-indigo-600 border-gray-300 rounded"
                      required
                    />
                    <label htmlFor="answer-true">True</label>
                  </span>
                  <span className="flex items-center space-x-2">
                    <input
                      id="answer-false"
                      type="radio"
                      checked={answer === "false"}
                      onChange={() => setAnswer("false")}
                      className="h-4 w-4 text-indigo-600 border-gray-300 rounded"
                      required
                    />
                    <label htmlFor="answer-false">False</label>
                  </span>
                </div>)
                :
                <textarea
                  ref={answerRef}
                  id="answer"
                  value={answer}
                  onChange={(e) => setAnswer(e.target.value)}
                  className="flex w-full overflow-hidden border border-gray-300 rounded-md p-2"
                  required
                />
              }
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
            <NewElementButton
              element={{
                  type_element: "ex",
                  id: "",
                  exercise_type: exerciseType,
                  question: question,
                  support: support+"\n<image_url>"+imageUrl+"</image_url>",
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