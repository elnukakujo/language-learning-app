"use client";

import type Exercise from "@/interface/Exercise";
import { useState } from "react";

export default function FillInTheBlankExercise({exercise}: { exercise: Exercise }) {
    const { question, support = '', answer } = exercise;
    const normalize = (str: string) => str.toLowerCase().replace(/[^a-z0-9]/g, '');
  
    // Parse answer with double underscore separator
    const correctAnswers = answer.split('__').map(a => a.trim()).filter(Boolean);
    
    // Initialize state
    const [userAnswers, setUserAnswers] = useState<string[]>(
        Array(correctAnswers.length).fill('')
    );
    
    const [isSubmitted, setIsSubmitted] = useState<boolean>(false);
    const [attempts, setAttempts] = useState<number>(0);
    const [isCorrect, setIsCorrect] = useState<boolean>(false);

    // Split support text using double underscore as blank markers
    const parts = support.split('__');

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        setIsSubmitted(true);
        if (normalize(correctAnswers.join('__')) === normalize(userAnswers.join('__'))) {
            setIsCorrect(true);
        } else {
            setAttempts(prev => prev + 1);
        };
    };

    const handleAnswerChange = (index: number, value: string) => {
        const newAnswers = [...userAnswers];
        newAnswers[index] = value;
        setUserAnswers(newAnswers);
    };

  return (
    <form className="flex flex-col space-y-4">
        {question && (
        <h3>{question}</h3>
        )}
        <p>
          {parts.map((part, index) => (
            <span key={index}>
              {part}
              {index < parts.length - 1 && (
                <input
                  type="text"
                  value={userAnswers[index]}
                  onChange={(e) => handleAnswerChange(index, e.target.value)}
                  className={`border-b-2 mx-1 w-24 text-center ${isSubmitted && 
                    (isCorrect ? 'border-green-500 text-green-700' : 'border-red-500 text-red-700')}`}
                  disabled={isSubmitted && isCorrect}
                  aria-label={`Blank ${index + 1}`}
                />
              )}
            </span>
          ))}
        </p>

        {!isSubmitted || !isCorrect ? (
          <button 
            type="button" 
            onClick={handleSubmit}
            className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors"
            disabled={isSubmitted && isCorrect}
          >
            {isSubmitted ? 'Try Again' : 'Check Answers'}
          </button>
        ) : null}

        {isSubmitted && (
          <div className={`mt-4 p-3 rounded-lg ${isCorrect ? 
            'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
            {isCorrect ? '✓ Correct! Well done!' : `✗ Some answers are incorrect (Attempt ${attempts}/3)`}
            
            {attempts >= 3 && !isCorrect && (
              <div className="mt-2">
                <p className="font-medium">Correct answers:</p>
                <div className="flex gap-2 mt-1">
                  {correctAnswers.map((ans, i) => (
                    <span key={i} className="bg-gray-100 px-2 py-1 rounded">
                      {ans}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}
    </form>
  );
}