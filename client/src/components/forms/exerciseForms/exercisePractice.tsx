"use client";

import Exercise from "@/interface/features/Exercise";
import { useEffect, useState } from "react";

import EssayExercise from "./essayExercise";
import BackButton from "@/components/buttons/backButton";
import AnsweringExercise from "./answeringExercise";
import FillInTheBlankExercise from "./fillInTheBlankExercise";
import MatchingExercise from "./matchingExercise";
import OrganizeExercise from "./organizeExercise";
import TranslateExercise from "./translateExercise";
import TrueFalseExercise from "./trueFalseExercise";

export default function ExercisePractice( { exercise_lists } : { exercise_lists: Exercise[] }) {
    const [currentIndex, setCurrentIndex] = useState<number>(0);
    const [currentExercise, setCurrentExercise] = useState<Exercise>(exercise_lists[currentIndex]);

    useEffect(() => {
        setCurrentExercise(exercise_lists[currentIndex]);
    }, [currentIndex]);

    return (
        <div>
            <h3>{currentIndex + 1} / {exercise_lists.length}</h3>
            {currentExercise.exercise_type === 'essay' && <EssayExercise exercise={currentExercise} />}
            {currentExercise.exercise_type === 'answering' && <AnsweringExercise exercise={currentExercise} />}
            {currentExercise.exercise_type === 'fill_in_the_blank' && <FillInTheBlankExercise exercise={currentExercise} />}
            {currentExercise.exercise_type === 'matching' && <MatchingExercise exercise={currentExercise} />}
            {currentExercise.exercise_type === 'organize' && <OrganizeExercise exercise={currentExercise} />}
            {currentExercise.exercise_type === 'translate' && <TranslateExercise exercise={currentExercise} />}
            {currentExercise.exercise_type === 'true_false' && <TrueFalseExercise exercise={currentExercise} />}
            {currentIndex < exercise_lists.length - 1 ? (<button 
                className="bg-blue-500 text-white rounded-md p-2"
                onClick={() => setCurrentIndex(currentIndex+1)}>
                Next Exercise
            </button>) : (
                <span>
                    <p>You have completed all exercises!</p>
                    <BackButton>
                        <p>Back to Unit</p>
                    </BackButton>
                </span>
            )}
        </div>
    );
}