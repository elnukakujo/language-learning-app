"use client";

import type Grammar from "@/interface/features/Grammar";
import { useEffect, useState } from "react";
import { updateScoreById } from "@/api/process";
import BackButton from "../../buttons/backButton";
import GrammarCard from "../grammarCard";
import ElementTagsCard from "../elementCards/elementTagsCard";
import SentenceCard from "../componentCards/sentenceCard";
import ElementPerformanceCard from "../elementCards/elementPerformanceCard";
import ElementSourcesCard from "../elementCards/elementSourcesCard";
import WordCard from "../componentCards/wordCard";

export default function GrammarFlashCard({ grammars }: { grammars: Grammar[] }) {
    const [currentIndex, setCurrentIndex] = useState<number>(0);
    let grammar: Grammar = grammars[currentIndex];

    useEffect(() => {
        grammar = grammars[currentIndex];
    }, [currentIndex]);


    const handleGoNext = () => {
        setCurrentIndex(currentIndex + 1);
        updateScoreById(grammar.id!, 1);
    }

    return (
        <article>
            <h3>{currentIndex + 1} / {grammars.length}</h3>
            <section className="flex flex-col space-y-4">
                <h1>Grammar Sheet</h1>
                <GrammarCard grammar={grammar}/>
                {grammar.example_words && grammar.example_words.length > 0 && (
                    <section className="flex flex-col space-y-4 items-baseline">
                        <h3>Example Words</h3>
                        {grammar.example_words.map((word, index) => (
                            <WordCard key={index} word={word}/>
                        ))}
                    </section>
                )}
                {grammar.example_sentences && grammar.example_sentences.length > 0 && (
                    <section className="flex flex-col space-y-4 items-baseline">
                        <h3>Example Sentences</h3>
                        {grammar.example_sentences.map((sentence, index) => (
                            <SentenceCard key={index} sentence={sentence}/>
                        ))}
                    </section>
                )}
                <ElementTagsCard element={grammar}/>
                <ElementSourcesCard element={grammar}/>
                <ElementPerformanceCard element={grammar} />
            </section>
            {currentIndex < grammars.length - 1 ? (
                <button className="bg-blue-500 text-white rounded-md p-2" onClick={() => handleGoNext()}>
                    <p>Next Grammar</p>
                </button>
            ) : (
                <BackButton>
                    <p>Back to Lesson</p>
                </BackButton>
            )}
        </article>
    );
}