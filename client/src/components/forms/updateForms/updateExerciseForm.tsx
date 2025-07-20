"use client";

import { useState } from "react";
import UpdateButton from "@/components/buttons/updateButton";
import type Exercise from "@/interface/Exercise";

export default function UpdateExerciseForm({ exercise }: { exercise: Exercise }) {
    const [question, setQuestion] = useState<string>(exercise.question);
    const [support, setSupport] = useState<string>(exercise.support || '');
    const [answer, setAnswer] = useState<string>(exercise.answer);

    return (
      <form className="flex flex-col space-y-4">
          <div className="flex flex-col space-y-2 h-fit">
            {[question, support, answer].map((value, index) => (
                <div key={index}>
                    <label htmlFor={`field-${index}`} key={index}>
                        {["Question*", "Support", "Answer*"][index]}
                    </label>
                    <textarea
                        value={value}
                        onChange={(e) => {
                            const newValue = e.target.value;
                            if (index === 0) setQuestion(newValue);
                            if (index === 1) setSupport(newValue);
                            if (index === 2) setAnswer(newValue);
                        }}
                        className="flex w-full overflow-hidden border border-gray-300 rounded-md p-2"
                    />
                </div>
              ))}
          </div>

        <UpdateButton
          element={{
              type_element: "ex",
              id: exercise.id,
              exercise_type: exercise.exercise_type,
              question: question,
              support: support,
              answer: answer,
              score: exercise.score,
              last_seen: exercise.last_seen,
              unit_id: exercise.unit_id
          }}
        />
      </form>
    );
}