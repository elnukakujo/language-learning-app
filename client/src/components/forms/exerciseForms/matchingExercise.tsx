"use client";

import type Exercise from "@/interface/Exercise";
import { useEffect, useState } from "react";
import Image from 'next/image';
import Markdown from "react-markdown";
import { updateScoreById } from "@/api";
import shuffle from 'lodash/shuffle';

type Item = {
    value: string;
    column: number;
};

export default function MatchingExercise({ exercise }: { exercise: Exercise }) {
    const { support = '', answer } = exercise;

    const pairs: Item[][] = answer.split("\n")
        .map(pair => pair.split("__"))
        .map(row =>
            row.map((value, colIndex) => ({ value, column: colIndex }))
        );

    const [remainingPairs, setRemainingPairs] = useState<Item[][]>(pairs);

    const numColumns = pairs[0].length;

    const [shuffledPairs, setShuffledPairs] = useState<Item[][]>([]);

    useEffect(() => {
        // Shuffle each column independently
        const shuffledColumns = Array.from({ length: numColumns }, (_, colIndex) => {
            const column = pairs.map(row => row[colIndex]);
            return shuffle(column); // lodash shuffle
        });

        // Reconstruct rows from shuffled columns
        const newPairs: Item[][] = pairs.map((_, rowIndex) =>
            shuffledColumns.map(column => column[rowIndex])
        );

        setShuffledPairs(newPairs);
    }, []);

    const imageUrl = support.match(/<image_url>(.*?)<\/image_url>/)?.[1] || null;
    const supportText = support.replace(/<image_url>.*?<\/image_url>/, '').trim();

    const [attempts, setAttempts] = useState<number>(3);
    const [selection, setSelection] = useState<Array<Item>>([]);

    const handleClick = (item: Item) => {
        // Remove old selection from the same column
        const updatedSelection = selection.filter(sel => sel.column !== item.column);

        const newSelection = [...updatedSelection, item];

        // Build string from values
        const newSelectionString = newSelection.map(sel => sel.value).join('');

        // Check against full pairs and partial prefixes
        const isFullMatch = remainingPairs.some(pair =>
            pair.map(p => p.value).join('') === newSelectionString
        );

        const isPartialMatch = remainingPairs.some(pair =>
            pair.map(p => p.value).join('').startsWith(newSelectionString)
        );
        if (isFullMatch) {
            if (remainingPairs.length === 1) {
                setIsSuccess(true);
            }
            // Remove the full matched pair from remainingPairs
            setRemainingPairs(prevRemaining =>
                prevRemaining.filter(pair => pair.map(p => p.value).join('') !== newSelectionString)
            );
            setSelection([]);
        } else if (isPartialMatch) {
            setSelection(newSelection);
        } else {
            setAttempts(prev => prev - 1);
            setSelection([]);
        }
    };

    const [isSuccess, setIsSuccess] = useState<boolean>(false);

    useEffect(() => {
        if (isSuccess) {
            updateScoreById(exercise.id, true).catch(console.error);
        };
    }, [isSuccess]);

    return (
        <form className="flex flex-col space-y-4">
            <h1>Match the pairs</h1>

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

            {(!isSuccess && attempts > 0) && 
                <section className="w-[32rem] mx-auto flex flex-row space-x-5">
                    {Array.from({ length: numColumns }, (_, colIndex) => (
                        <div key={colIndex} className="flex flex-col space-y-2 justify-around mb-2">
                            {shuffledPairs.map((row, rowIndex) => {
                                const item = row[colIndex];
                                return (
                                    <button
                                        type="button"
                                        key={rowIndex}
                                        onClick={() => handleClick(item)}
                                        className={`w-fit border-2 rounded px-4 py-2 ${selection.includes(item) ? 'bg-blue-500 text-black border-blue-500' : ''} transition-colors duration-300 ${!remainingPairs.some(pair => pair.some(p => p.value === item.value && p.column === item.column)) ? 'opacity-50 cursor-not-allowed' : ''}`}
                                        disabled={
                                            !remainingPairs.some(pair => pair.some(p => p.value === item.value && p.column === item.column)) ||
                                            selection.map(sel => sel.column).includes(colIndex) ||
                                            attempts < 0
                                        }
                                    >
                                        {item.value}
                                    </button>
                                );
                            })}
                        </div>
                    ))}
                </section>
            }

            {attempts <= 2 && attempts > 0 && !isSuccess && (
                <div className={`mt-4 p-3 rounded-lg bg-red-100 text-red-800`}>
                    <p>✗ Some answers are incorrect (Attempts left {attempts}/3)</p>
                </div>
            )}

            {attempts < 0 && (
                <div className={`mt-4 p-3 rounded-lg bg-red-100 text-red-800`}>
                    <p>Out of attempts! The correct pairs were the following:</p>
                    <ul>
                        {pairs.map((pair, index) => (
                            <li key={index}>{pair.map(item => item.value).join(' - ')}</li>
                        ))}
                    </ul>
                </div>
            )}

            {isSuccess && (
                <div className={`mt-4 p-3 rounded-lg bg-green-100 text-green-800`}>
                    <p>✓ Correct! Well done!</p>
                </div>
            )}
        </form>
    );
}