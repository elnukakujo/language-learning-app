"use client";

import { useState, useEffect } from "react";
import NewElementButton from "@/components/buttons/newElementButton";
import ClassicSelectMenu from "@/components/selectMenu/classicSelectMenu";
import OpenCloseMenu from "@/components/selectMenu/openCloseMenu";
import ImageLoader from "@/components/imageLoader";

import AutoSizeTextArea from "@/components/textArea/autoSizeTextArea";
import TrueFalseInput from "@/components/input/trueFalseInput";
import DiscreteInput from "@/components/input/discreteInput";

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
    calligraphies: {
        items: Array<{
            id: string;
            character: string;
            meaning: string;
        }>;
        count: number;
    };
}

export default function CreateExerciseForm({ unit_id, unitElements }: { unit_id: string, unitElements: UnitElements }) {
    const [exerciseType, setExerciseType] = useState<'essay' | 'answering' | 'translate' | 'organize' | 'fill_in_the_blank' | 'matching' | 'true_false' | "">("")
    const [question, setQuestion] = useState<string>("")
    const [answer, setAnswer] = useState<string>("")
    const [supportText, setSupportText] = useState<string>("")
    const [imageUrl, setImageUrl] = useState<string | null>(null);

    const [vocAssociated, setVocAssociated] = useState<string[]>([]);
    const [callAssociated, setCallAssociated] = useState<string[]>([]);
    const [gramAssociated, setGramAssociated] = useState<string[]>([]);

    useEffect(() => {
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
            "fill_in_the_blank",
            "essay",
            "true_false",
            "organize",
            "answering",
            "matching"
          ]}
          selectedOption={exerciseType}
          onChange={(value) => setExerciseType(value as typeof exerciseType)}
        />
        {exerciseType !== "" && (
          <>
            {!["matching", "organize"].includes(exerciseType) && <AutoSizeTextArea
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              className="flex w-full overflow-hidden border border-gray-300 rounded-md p-2"
              label="Question"
            />}

            <AutoSizeTextArea
              value={supportText}
              onChange={(e) => setSupportText(e.target.value)}
              className="flex w-full overflow-hidden border border-gray-300 rounded-md p-2"
              label="Support"
            />
            <ImageLoader previewUrl={imageUrl} setPreviewUrl={setImageUrl} />
            
            {exerciseType === "true_false" && 
              <TrueFalseInput
                value={answer === "true"}
                onChange={(e) => setAnswer(e.target.value)}
                label="Answer"
              />
            }

            {["matching", "organize"].includes(exerciseType) && 
              <DiscreteInput
                value={answer}
                setValue={setAnswer}
                label="Answer"
                is2D={exerciseType === "matching"}
              />
            }

            { !["true_false", "matching", "organize"].includes(exerciseType) && 
              <AutoSizeTextArea
                value={answer}
                onChange={(e) => setAnswer(e.target.value)}
                label="Answer"
              />
            }
            
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
                elements={unitElements.calligraphies.items.map(item => ({id: item.id, value: item.character + " - " + item.meaning}))}
                selectedElements={callAssociated}
                setSelectedElements={setCallAssociated}
                label="Associated Calligraphies"
              />
            </section>
            <NewElementButton
              element={{
                  exercise_type: exerciseType,
                  question: question,
                  text_support: supportText,
                  image_files: imageUrl ? [imageUrl] : [],
                  answer: answer,
                  score: 0.0,
                  last_seen: new Date().toISOString(),
                  unit_id: unit_id,
                  vocabulary_ids: vocAssociated,
                  grammar_ids: gramAssociated,
                  calligraphy_ids: callAssociated
              }}
              type="ex"
            />
          </>
        )}
      </form>
    );
}