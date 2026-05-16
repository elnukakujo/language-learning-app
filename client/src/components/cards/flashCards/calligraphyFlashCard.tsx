"use client";

import { updateScoreById } from "@/api";
import { useEffect, useState } from "react";
import Calligraphy from "@/interface/features/Calligraphy";
import BackButton from "../buttons/backButton";
import CharacterCard from "../componentCards/characterCard";
import WordCard from "../componentCards/wordCard";
import SentenceCard from "../componentCards/sentenceCard";
import ElementTagsCard from "../elementCards/elementTagsCard";
import ElementSourcesCard from "../elementCards/elementSourcesCard";
import ElementPerformanceCard from "../elementCards/elementPerformanceCard";

export default function CalligraphyFlashCard({ calligraphies }: { calligraphies: Calligraphy[] }) {
    const [currentIndex, setCurrentIndex] = useState<number>(0);
    let calligraphy: Calligraphy = calligraphies[currentIndex];

    useEffect(() => {
        calligraphy = calligraphies[currentIndex];
    }, [currentIndex]);
        
    const [hiddenTranslation, setHiddenTranslation] = useState<boolean>(true);
    const [graded, setGraded] = useState<boolean>(false);
    const [hiddenAdditionalInformations, setHiddenAdditionalInformations] = useState<boolean>(true);

    const handleGrade = (isCorrect: boolean) => {
        setGraded(true);
        updateScoreById(calligraphy.id!, isCorrect ? 1 : 0);
    };

    const handleGoNext = () => {
        setCurrentIndex(currentIndex + 1);
        setHiddenTranslation(true);
        setGraded(false);
        setHiddenAdditionalInformations(true);
    }

    return (
        <article>
            <h3>{currentIndex + 1} / {calligraphies.length}</h3>
            <section className="flex flex-col space-y-4">
                <h1>Calligraphy Sheet</h1>
                <CharacterCard character={calligraphy.character} hiddenTranslation={hiddenTranslation} hiddenAdditionalInformations={hiddenAdditionalInformations}/>
                
                {!hiddenAdditionalInformations && calligraphy.example_words && (
                    <section className="flex flex-col space-y-4 items-baseline">
                        <h3>Example Words</h3>
                        {calligraphy.example_words.map((word, index) => (
                            <WordCard key={index} word={word} hiddenTranslation={hiddenTranslation} hiddenAdditionalInformations={true}/>
                        ))}
                    </section>
                )}
                {!hiddenAdditionalInformations && calligraphy.example_sentences && (
                    <section className="flex flex-col space-y-4 items-baseline">
                        <h3>Example Sentences</h3>
                        {calligraphy.example_sentences.map((sentence, index) => (
                            <SentenceCard key={index} sentence={sentence} hiddenTranslation={hiddenTranslation}/>
                        ))}
                    </section>
                )}
                <ElementTagsCard element={calligraphy}/>
                <ElementSourcesCard element={calligraphy}/>
                <ElementPerformanceCard element={calligraphy} />
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
                currentIndex < calligraphies.length - 1 ? (
                    <button className="bg-blue-500 text-white rounded-md p-2" onClick={() => handleGoNext()}>
                        <p>Next Calligraphy</p>
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