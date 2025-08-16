import GrammarFlashCard from "@/components/cards/grammarFlashCard";
import type Grammar from "@/interface/Grammar";
import { getElementbyId, getNext } from "@/api";
import NavButton from "@/components/buttons/navButton";

type paramsType = {
    language_id: string;
    unit_id: string;
    gram_id: string;
};

export default async function GrammarFlashCardPage({ params }: { params: paramsType }) {
    const { language_id, unit_id, gram_id } = await params;
    
    const grammar: Grammar = await getElementbyId(gram_id);
    const next_gram_id: string = await getNext(gram_id);
    
    return (
        <main>
            <header>
                <h2>Grammar Flashcard</h2>
            </header>
            <GrammarFlashCard grammar={grammar} />
            <NavButton path={`/languages/${language_id}/unit/${unit_id}/gram/${next_gram_id}/flashcard`}>
                <p>Next Grammar</p>
            </NavButton>
        </main>
    );
}