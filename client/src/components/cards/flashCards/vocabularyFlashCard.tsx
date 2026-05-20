"use client";

import BackButton from "@/components/buttons/backButton";
import { updateScoreById } from "@/api/process";
import { useEffect, useState } from "react";
import type Vocabulary from "@/interface/features/Vocabulary";
import WordCard from "../componentCards/wordCard";
import SentenceCard from "../componentCards/sentenceCard";
import ElementPerformanceCard from "../elementCards/elementPerformanceCard";
import ElementSourcesCard from "../elementCards/elementSourcesCard";
import ElementTagsCard from "../elementCards/elementTagsCard";

export default function VocabularyFlashCard({ vocabularies }: { vocabularies: Vocabulary[] }) {
    const [currentIndex, setCurrentIndex] = useState<number>(0);
    let vocabulary: Vocabulary = vocabularies[currentIndex];

    useEffect(() => {
        vocabulary = vocabularies[currentIndex];
    }, [currentIndex]);

    const [hiddenTranslation, setHiddenTranslation] = useState<boolean>(true);
    const [graded, setGraded] = useState<boolean>(false);
    const [hiddenAdditionalInformations, setHiddenAdditionalInformations] = useState<boolean>(true);
    const handleGrade = (isCorrect: boolean) => {
        setGraded(true);
        updateScoreById(vocabulary.id!, isCorrect ? 1 : 0);
    };

    const handleGoNext = () => {
        setCurrentIndex(currentIndex + 1);
        setHiddenTranslation(true);
        setGraded(false);
        setHiddenAdditionalInformations(true);
    }
    return (
        <article>
            <h3>{currentIndex + 1} / {vocabularies.length}</h3>
            <section className="flex flex-col space-y-4">
                <h1>Vocabulary Sheet</h1>
                <WordCard word={vocabulary.word} hiddenTranslation={hiddenTranslation} hiddenAdditionalInformations={hiddenAdditionalInformations}/>
                {!hiddenAdditionalInformations && vocabulary.example_sentences && (
                    <section className="flex flex-col space-y-4 items-baseline">
                        <h3>Example Sentences</h3>
                        {vocabulary.example_sentences.map((sentence, index) => (
                            <SentenceCard key={index} sentence={sentence} hiddenTranslation={hiddenTranslation}/>
                        ))}
                    </section>
                )}
                <ElementTagsCard element={vocabulary}/>
                <ElementSourcesCard element={vocabulary}/>
                <ElementPerformanceCard element={vocabulary} />
            </section>
            <section className="flex flex-row space-x-4">
                {hiddenTranslation ? (
                    <>
                        <button className="bg-yellow-500 text-white rounded-md p-2" onClick={() => setHiddenAdditionalInformations(!hiddenAdditionalInformations)}>
                            {hiddenAdditionalInformations ? "Show Additional Informations" : "Hide Additional Informations"}
                        </button>
                        <button className="bg-blue-500 text-white rounded-md p-2" onClick={() => { setHiddenTranslation(false); }}>
                            Show Translation
                        </button>
                    </>
                ) : (
                    !graded && (
                        <>
                            <button className="bg-green-500 text-white rounded-md p-2" onClick={() => handleGrade(true)}>
                                Correct?
                            </button>
                            <button className="bg-red-500 text-white rounded-md p-2" onClick={() => handleGrade(false)}>
                                Wrong?
                            </button>
                        </>
                    )
                )}
            </section>
            {graded && (
                currentIndex < vocabularies.length - 1 ? (
                    <button className="bg-blue-500 text-white rounded-md p-2" onClick={() => handleGoNext()}>
                        <p>Next Vocabulary</p>
                    </button>
                ) : (
                    <BackButton>
                        <p>Back to Lesson</p>
                    </BackButton>
                )
            )}
        </article>
    );
}