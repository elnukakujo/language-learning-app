import Vocabulary from "@/interface/features/Vocabulary";
import { getVocabularyByLesson } from "@/api/vocabulary";
import VocabularyFlashCard from "@/components/cards/flashCards/vocabularyFlashCard";

export default async function VocabularyFlashCardPage({ params }: { params: { language_id: string; lesson_id: string; voc_id: string }}) {
    const { lesson_id } = await params;

    const vocabularies: Vocabulary[] = await getVocabularyByLesson(lesson_id);
    vocabularies.sort(() => Math.random() - 0.5); // Shuffle the array randomly

    return (
        <main>
            <h1>Vocabulary Flashcard</h1>
            <VocabularyFlashCard vocabularies={vocabularies} />
        </main>
    );
}