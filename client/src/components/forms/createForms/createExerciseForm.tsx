"use client";

import { useState } from "react";
import NewElementButton from "@/components/buttons/newElementButton";

export default function CreateExerciseForm({ unit_id }: { unit_id: string }) {
    const [exerciseType, setExerciseType] = useState<string>("")
    const [question, setQuestion] = useState<string>("")
    const [answer, setAnswer] = useState<string>("")    

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

        <NewElementButton
          element={{
              type_element: "ex",
              id: "",
              exercise_type: exerciseType,
              question: question,
              support: "",
              answer: answer,
              score: 0.0,
              last_seen: new Date,
              unit_id: unit_id
          }}
        />
      </form>
    );
}