import Vocabulary from "@/interface/Vocabulary";
import { getElementbyId, getNext } from "@/api";
import VocabularyFlashCard from "@/components/cards/vocabularyFlashCard";
import NavButton from "@/components/buttons/navButton";

export default async function VocabularyFlashCardPage({ params }: { params: { language_id: string; unit_id: string; voc_id: string }}) {
    const { language_id, unit_id, voc_id } = await params;

    const vocabulary: Vocabulary = await getElementbyId(voc_id);
    const next_voc_id: string = await getNext(voc_id);

    return (
        <main>
            <h1>Vocabulary Flashcard</h1>
            <VocabularyFlashCard vocabulary={vocabulary} />
            <NavButton path={`/languages/${language_id}/unit/${unit_id}/voc/${next_voc_id}/flashcard`}>
                <p>Next Vocabulary</p>
            </NavButton>
        </main>
    );
}