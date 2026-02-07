import Vocabulary from "@/interface/features/Vocabulary";
import { getVocabularyByUnit } from "@/api";
import VocabularyFlashCard from "@/components/cards/vocabularyFlashCard";

export default async function VocabularyFlashCardPage({ params }: { params: { language_id: string; unit_id: string; voc_id: string }}) {
    const { language_id, unit_id } = await params;

    const vocabularies: Vocabulary[] = await getVocabularyByUnit(unit_id);
    vocabularies.sort(() => Math.random() - 0.5); // Shuffle the array randomly

    return (
        <main>
            <h1>Vocabulary Flashcard</h1>
            <VocabularyFlashCard vocabularies={vocabularies} />
        </main>
    );
}