"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import NewElementButton from "@/components/buttons/newElementButton";
import ClassicSelectMenu from "@/components/selectMenu/classicSelectMenu";
import OpenCloseMenu from "@/components/selectMenu/openCloseMenu";
import AutoSizeTextArea from "@/components/textArea/autoSizeTextArea";
import TrueFalseInput from "@/components/input/trueFalseInput";
import DiscreteInput from "@/components/input/discreteInput";
import { createExercise } from "@/api";
import Calligraphy from "@/interface/features/Calligraphy";
import Grammar from "@/interface/features/Grammar";
import Vocabulary from "@/interface/features/Vocabulary";
import MediaLoader from "@/components/mediaLoader";
import Exercise from "@/interface/features/Exercise";

interface UnitElements {
    vocabularies: Vocabulary[];
    grammars: Grammar[];
    calligraphies: Calligraphy[];
}

export default function CreateExerciseForm({ unit_id, unitElements }: { unit_id: string, unitElements: UnitElements }) {
    const router = useRouter();
    
    const [exerciseType, setExerciseType] = useState<'essay' | 'answering' | 'translate' | 'organize' | 'fill_in_the_blank' | 'matching' | 'true_false' | undefined>(undefined)
    const [question, setQuestion] = useState<string | undefined>(undefined)
    const [answer, setAnswer] = useState<string | undefined>(undefined)
    const [supportText, setSupportText] = useState<string | undefined>(undefined); 
    const [imageUrl, setImageUrl] = useState<string | undefined>(undefined);
    const [audioUrl, setAudioUrl] = useState<string | undefined>(undefined);

    useEffect(() => {
      console.log(imageUrl)
    }, [imageUrl]);

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

    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
      e.preventDefault();
      
      // Extract language_id from current URL
      const currentPath = window.location.pathname;
      const pathParts = currentPath.split('/');
      const languageId = pathParts[2]; // From /languages/LANG_ID/...
      
      const element: Exercise = {
        exercise_type: exerciseType as Exclude<typeof exerciseType, "">,
        question: question!,
        text_support: supportText || undefined,
        image_files: imageUrl ? [imageUrl] : [],
        audio_files: audioUrl ? [audioUrl] : [],
        answer: answer!,
        unit_id: unit_id,
        vocabulary_ids: vocAssociated,
        grammar_ids: gramAssociated,
        calligraphy_ids: callAssociated
      };
      
      try {
        await createExercise(element);
        
        const router_path = `/languages/${languageId}/unit/${unit_id}`;
        
        router.push(router_path);
        router.refresh();
        
      } catch (error) {
        console.error("Failed to create exercise:", error);
        alert("Failed to create exercise. Check console for details.");
      }
    };

    return (
      <form className="flex flex-col space-y-4 items-center min-w-[40rem]" onSubmit={handleSubmit}>
        <ClassicSelectMenu
          label="Exercise Type"
          options={[
            "translate",
            "fill_in_the_blank",
            "essay",
            "true_false",
            "organize",
            "answering",
            "matching"
          ]}
          selectedOption={exerciseType || ""}
          onChange={(value) => setExerciseType(value as typeof exerciseType)}
          required={true}
        />
        {exerciseType !== undefined && (
          <>
            {!["matching", "organize"].includes(exerciseType) && <AutoSizeTextArea
              value={question || ""}
              onChange={(e) => setQuestion(e.target.value)}
              className="flex w-full overflow-hidden border border-gray-300 rounded-md p-2"
              label="Question"
              required={true}
            />}

            <AutoSizeTextArea
              value={supportText || ""}
              onChange={(e) => setSupportText(e.target.value)}
              className="flex w-full overflow-hidden border border-gray-300 rounded-md p-2"
              label="Support"
            />
            <MediaLoader imageUrl={imageUrl} setImageUrl={setImageUrl} audioUrl={audioUrl} setAudioUrl={setAudioUrl} />
            
            {exerciseType === "true_false" && 
              <TrueFalseInput
                value={answer === "true"}
                onChange={(e) => setAnswer(e.target.value)}
                label="Answer"
              />
            }

            {["matching", "organize"].includes(exerciseType) && 
              <DiscreteInput
                value={answer || ""}
                setValue={setAnswer}
                label="Answer"
                is2D={exerciseType === "matching"}
              />
            }

            { !["true_false", "matching", "organize"].includes(exerciseType) && 
              <AutoSizeTextArea
                value={answer || ""}
                onChange={(e) => setAnswer(e.target.value)}
                label="Answer"
                required={true}
              />
            }
            
            <section className="flex flex-col space-y-4 w-full items-baseline">
              <OpenCloseMenu
                elements={unitElements.vocabularies.map(item => ({id: item.id!, value: item.word.word + " - " + item.word.translation}))}
                selectedElements={vocAssociated}
                setSelectedElements={setVocAssociated}
                label="Associated Vocabulary"
              />
              <OpenCloseMenu
                elements={unitElements.grammars.map(item => ({id: item.id!, value: item.title}))}
                selectedElements={gramAssociated}
                setSelectedElements={setGramAssociated}
                label="Associated Grammar"
              />
              <OpenCloseMenu
                elements={unitElements.calligraphies.map(item => ({id: item.id!, value: item.character.character + " - " + item.character.phonetic}))}
                selectedElements={callAssociated}
                setSelectedElements={setCallAssociated}
                label="Associated Calligraphies"
              />
            </section>
            <NewElementButton>Add Exercise</NewElementButton>
          </>
        )}
      </form>
    );
}