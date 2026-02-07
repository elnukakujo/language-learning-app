import GrammarFlashCard from "@/components/cards/grammarFlashCard";
import type Grammar from "@/interface/features/Grammar";
import { getGrammarByUnit } from "@/api";

type paramsType = {
    language_id: string;
    unit_id: string;
};

export default async function GrammarFlashCardPage({ params }: { params: paramsType }) {
    const { language_id, unit_id } = await params;
    
    const grammars: Grammar[] = await getGrammarByUnit(unit_id);
    grammars.filter(grammar => grammar.learnable_sentences && grammar.learnable_sentences.length > 0)
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