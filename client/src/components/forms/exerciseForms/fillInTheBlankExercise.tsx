"use client";

import { updateScoreById } from "@/api";
import type Exercise from "@/interface/Exercise";
import { useEffect, useState } from "react";
import Image from 'next/image';
import Markdown from "react-markdown";
import AutoWidthInput from "@/components/input/autoWidthInput";

export default function FillInTheBlankExercise({exercise}: { exercise: Exercise }) {
    const { question, support = '', answer } = exercise;
    const normalize = (str: string) => str.toLowerCase();

    const imageUrl = support.match(/<image_url>(.*?)<\/image_url>/)?.[1] || null;
    const supportText = support.replace(/<image_url>.*?<\/image_url>/, '').trim();
  
    // Parse answer with double underscore separator
    const correctAnswers = answer.split('__').map(a => a.trim()).filter(Boolean);
    
    // Initialize state
    const [userAnswers, setUserAnswers] = useState<string[]>(
        Array(correctAnswers.length).fill('')
    );
    
    const [isSubmitted, setIsSubmitted] = useState<boolean>(false);
    const [attempts, setAttempts] = useState<number>(0);

    const parts = question.split('__');
    const [isCorrect, setIsCorrect] = useState<boolean[]>(Array(parts.length-1).fill(false));

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        setIsSubmitted(true);
        userAnswers.forEach((answer, index) => {
            if (normalize(correctAnswers[index]) === normalize(answer)) {
                setIsCorrect(prev => {
                    const newIsCorrect = [...prev];
                    newIsCorrect[index] = true;
                    return newIsCorrect;
                });
            }
        });
        console.log(isCorrect);
    };
    useEffect(() => {
      if (isCorrect.every(val => val)) {
          updateScoreById(exercise.id, true).catch(console.error);
      } else {
          setAttempts(prev => prev + 1);
          if (attempts >= 2) {
              updateScoreById(exercise.id, false).catch(console.error);
          }
      };
    }, [isCorrect]);

    const handleAnswerChange = (index: number, value: string) => {
        const newAnswers = [...userAnswers];
        newAnswers[index] = value;
        setUserAnswers(newAnswers);
    };

  return (
    <form className="flex flex-col space-y-4">
        <Markdown>Fill in the blanks</Markdown>

        {support && (
            <>
                {supportText && <Markdown>{supportText}</Markdown>}
                {imageUrl && 
                    <Image 
                        src={imageUrl} 
                        alt="Support" 
                        className="mt-2" 
                        width={300}
                        height={300}
                    />}
            </> 
        )}
        <p>
          {parts.map((part, index) => (
            <span key={index}>
              {part}
              {index < parts.length - 1 && (
                <AutoWidthInput
                  value={userAnswers[index]}
                  onChange={(e) => handleAnswerChange(index, e.target.value)}
                  className={`border-b-2 mx-1 w-auto text-center ${
                    isSubmitted &&
                    (isCorrect[index]
                      ? 'border-green-500 text-green-700'
                      : 'border-red-500 text-red-700')
                  }`}
                  disabled={isSubmitted && isCorrect[index]}
                  aria-label={`Blank ${index + 1}`}
                />
                
              )}
            </span>
          ))}
        </p>

        {!isSubmitted || !isCorrect.every(val => val) ? (
          <button 
            type="button" 
            onClick={handleSubmit}
            className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors"
            disabled={isSubmitted && isCorrect.every(val => val)}
          >
            {isSubmitted ? 'Try Again' : 'Check Answers'}
          </button>
        ) : null}

        {isSubmitted && (
          <div className={`mt-4 p-3 rounded-lg ${isCorrect.every(val => val) ? 
            'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'}`}>
            {isCorrect.every(val => val) ? '✓ Correct! Well done!' : `✗ Some answers are incorrect (Attempt ${attempts}/3)`}
            
            {attempts >= 3 && !isCorrect.every(val => val) && (
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