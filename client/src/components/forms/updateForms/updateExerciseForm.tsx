"use client";

import { useState, useRef, useEffect } from "react";
import UpdateButton from "@/components/buttons/updateButton";
import ChangeUnitMenu from "@/components/selectMenu/changeUnitMenu";
import type Exercise from "@/interface/Exercise";

export default function UpdateExerciseForm({ exercise, existingUnitsId }: { exercise: Exercise, existingUnitsId: string[] }) {
    const [question, setQuestion] = useState<string>(exercise.question);
    const [support, setSupport] = useState<string>(exercise.support || '');
    const [answer, setAnswer] = useState<string>(exercise.answer);

    const [unitId, setUnitId] = useState<string>(exercise.unit_id);

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

    return (
      <form className="flex flex-col space-y-4">
          <div className="flex flex-col space-y-2 h-fit">
            <ChangeUnitMenu unitsId={existingUnitsId} unitId={unitId} onChange={setUnitId} />
            {[question, support, answer].map((value, index) => (
                <div key={index}>
                    <label htmlFor={`field-${index}`} key={index}>
                        {["Question*", "Support", "Answer*"][index]}
                    </label>
                    <textarea
                        ref={index === 0 ? questionRef : index === 1 ? supportRef : answerRef}
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
              unit_id: unitId
          }}
        />
      </form>
    );
}