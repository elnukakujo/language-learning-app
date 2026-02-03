"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/dist/client/components/navigation";
import UpdateButton from "@/components/buttons/updateButton";
import type Exercise from "@/interface/features/Exercise";
import Calligraphy from "@/interface/features/Calligraphy";
import Grammar from "@/interface/features/Grammar";
import Vocabulary from "@/interface/features/Vocabulary";
import { updateExercise } from "@/api";

import ImageLoader from "@/components/imageLoader";
import AutoSizeTextArea from "@/components/textArea/autoSizeTextArea";
import OpenCloseMenu from "@/components/selectMenu/openCloseMenu";
import ClassicSelectMenu from "@/components/selectMenu/classicSelectMenu";
import TrueFalseInput from "@/components/input/trueFalseInput";
import DiscreteInput from "@/components/input/discreteInput";

interface UnitElements {
    vocabularies: Vocabulary[];
    grammars: Grammar[];
    calligraphies: Calligraphy[];
}

export default function UpdateExerciseForm({ exercise, unitElements }: { exercise: Exercise, unitElements: UnitElements }) {
    const router = useRouter();

    const [updatedExerciseType, setUpdatedExerciseType] = useState<'essay' | 'answering' | 'translate' | 'organize' | 'fill_in_the_blank' | 'matching' | 'true_false' | undefined>(exercise.exercise_type || undefined);
    const [updatedQuestion, setUpdatedQuestion] = useState<string | undefined>(exercise.question || undefined);
    const [updatedAnswer, setUpdatedAnswer] = useState<string | undefined>(exercise.answer || undefined);
    const [updatedSupportText, setUpdatedSupportText] = useState<string | undefined>(exercise.text_support || undefined);
    const [updatedImageUrl, setUpdatedImageUrl] = useState<string | undefined>(exercise.image_files ? exercise.image_files[0] : undefined);
  
    useEffect(() => {
      console.log(updatedImageUrl)
    }, [updatedImageUrl]);

    const [vocAssociated, setVocAssociated] = useState<string[]>(exercise.vocabulary_ids || []);
    const [callAssociated, setCallAssociated] = useState<string[]>(exercise.calligraphy_ids || []);
    const [gramAssociated, setGramAssociated] = useState<string[]>(exercise.grammar_ids || []);
    
    useEffect(() => {
      switch (updatedExerciseType) {
        case "translate":
          setUpdatedQuestion("A sentence to translate");
          setUpdatedSupportText("");
          setUpdatedAnswer("The translation");
          break;
        case "fill_in_the_blank":
          setUpdatedQuestion("The house is __ and __.");
          setUpdatedSupportText("");
          setUpdatedAnswer("big__small");
          break;
        case "essay":
          setUpdatedQuestion("Write here some requirements about the essay, and details");
          setUpdatedSupportText("");
          setUpdatedAnswer("Some helps and tips to write the essay");
          break;
        case "true_false":
          setUpdatedQuestion("A statement to evaluate");
          setUpdatedSupportText("");
          setUpdatedAnswer("true");
          break;
        case "answering":
          setUpdatedQuestion("A question to answer");
          setUpdatedSupportText("");
          setUpdatedAnswer("The answer to the question");
          break;
        default:
          setUpdatedQuestion("");
          setUpdatedSupportText("");
          setUpdatedAnswer("");
          break;
      }
    }, [updatedExerciseType]); 

    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
      e.preventDefault();
      
      // Extract language_id from current URL
      const currentPath = window.location.pathname;
      const pathParts = currentPath.split('/');
      const languageId = pathParts[2]; // From /languages/LANG_ID/...
      
      const element = {
        exercise_type: updatedExerciseType as Exclude<typeof updatedExerciseType, "">,
        question: updatedQuestion,
        text_support: updatedSupportText || undefined,
        image_files: updatedImageUrl ? [updatedImageUrl] : [],
        audio_files: [],
        answer: updatedAnswer,
        unit_id: exercise.unit_id,
        vocabulary_ids: vocAssociated,
        grammar_ids: gramAssociated,
        calligraphy_ids: callAssociated
      };
      
      try {
        await updateExercise(exercise.id!, element);
        
        const router_path = `/languages/${languageId}/unit/${exercise.unit_id}/ex/${exercise.id}/`;
        
        router.push(router_path);
        router.refresh();
        
      } catch (error) {
        console.error("Failed to update exercise:", error);
        alert("Failed to update exercise. Check console for details.");
      }
    };

    return (
      <form className="flex flex-col space-y-4 items-center" onSubmit={handleSubmit}>
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
          selectedOption={updatedExerciseType || ""}
          onChange={(value) => setUpdatedExerciseType(value as typeof updatedExerciseType)}
          required={true}
        />
        {updatedExerciseType !== undefined && (
          <>
            {!["matching", "organize"].includes(updatedExerciseType) && <AutoSizeTextArea
              value={updatedQuestion || ""}
              onChange={(e) => setUpdatedQuestion(e.target.value)}
              className="flex w-full overflow-hidden border border-gray-300 rounded-md p-2"
              label="Question"
              required={true}
            />}

            <AutoSizeTextArea
              value={updatedSupportText || ""}
              onChange={(e) => setUpdatedSupportText(e.target.value)}
              className="flex w-full overflow-hidden border border-gray-300 rounded-md p-2"
              label="Support"
            />
            <ImageLoader imageUrl={updatedImageUrl} setImageUrl={setUpdatedImageUrl} />
            
            {updatedExerciseType === "true_false" && 
              <TrueFalseInput
                value={updatedAnswer === "true"}
                onChange={(e) => setUpdatedAnswer(e.target.value)}
                label="Answer"
              />
            }

            {["matching", "organize"].includes(updatedExerciseType) && 
              <DiscreteInput
                value={updatedAnswer || ""}
                setValue={setUpdatedAnswer}
                label="Answer"
                is2D={updatedExerciseType === "matching"}
              />
            }

            { !["true_false", "matching", "organize"].includes(updatedExerciseType) && 
              <AutoSizeTextArea
                value={updatedAnswer || ""}
                onChange={(e) => setUpdatedAnswer(e.target.value)}
                label="Answer"
                required={true}
              />
            }
            
            <section className="flex flex-col space-y-4 w-full items-baseline">
              <OpenCloseMenu
                elements={unitElements.vocabularies.map(item => ({id: item.id, value: item.word.word + " - " + item.word.translation}))}
                selectedElements={vocAssociated}
                setSelectedElements={setVocAssociated}
                label="Associated Vocabulary"
              />
              <OpenCloseMenu
                elements={unitElements.grammars.map(item => ({id: item.id, value: item.title}))}
                selectedElements={gramAssociated}
                setSelectedElements={setGramAssociated}
                label="Associated Grammar"
              />
              <OpenCloseMenu
                elements={unitElements.calligraphies.map(item => ({id: item.id, value: item.character.character + " - " + item.character.phonetic}))}
                selectedElements={callAssociated}
                setSelectedElements={setCallAssociated}
                label="Associated Calligraphies"
              />
            </section>
            <UpdateButton>Update Exercise </UpdateButton>
          </>
        )}
      </form>
    );
}