"use client";

import { useState } from "react";
import UpdateButton from "@/components/buttons/updateButton";
import type Exercise from "@/interface/Exercise";

export default function UpdateExerciseForm({ exercise }: { exercise: Exercise }) {
    const [exerciseType, setExerciseType] = useState<string>(exercise.exercise_type || "")
    const [question, setQuestion] = useState<string>(exercise.question)
    const [answer, setAnswer] = useState<string>(exercise.answer)    

    return (
      <form className="flex flex-col space-y-4">
          <div className="flex flex-col space-y-2 h-fit">
            {[exerciseType, question, answer].map((value, index) => (
                <div key={index}>
                    <label htmlFor={`field-${index}`} key={index}>
                        {["Exercise Type", "Question*", "Answer*"][index]}
                    </label>
                    <textarea
                        value={value}
                        onChange={(e) => {
                            const newValue = e.target.value;
                            if (index === 0) setExerciseType(newValue);
                            if (index === 1) setQuestion(newValue);
                            if (index === 2) setAnswer(newValue);
                        }}
                        className="flex overflow-hidden border border-gray-300 rounded-md p-2"
                    />
                </div>
              ))}
          </div>

        <UpdateButton
          element={{
              type_element: "ex",
              id: exercise.id,
              exercise_type: exerciseType,
              question: question,
              support: exercise.support,
              answer: answer,
              score: exercise.score,
              last_seen: exercise.last_seen,
              unit_id: exercise.unit_id
          }}
        />
      </form>
    );
}