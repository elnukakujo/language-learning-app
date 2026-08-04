import GrammarFlashCard from "@/components/elements/grammarFlashCard";
import type Grammar from "@/interface/features/Grammar";
import { getGrammarByLesson } from "@/api/grammar";

type paramsType = {
    language_id: string;
    lesson_id: string;
};

export default async function GrammarFlashCardPage({ params }: { params: Promise<paramsType> }) {
    const { lesson_id } = await params;
    
    const grammars: Grammar[] = await getGrammarByLesson(lesson_id);
    grammars.filter(grammar => grammar.example_sentences && grammar.example_sentences.length > 0)
    grammars.sort(() => Math.random() - 0.5); // Shuffle the array randomly
    
    return (
        <main>
            <header>
                <h2>Grammar Flashcard</h2>
            </header>
            <GrammarFlashCard grammars={grammars} />
        </main>
    );
}