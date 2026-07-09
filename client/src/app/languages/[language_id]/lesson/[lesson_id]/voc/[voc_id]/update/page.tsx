import type Vocabulary from "@/interface/features/Vocabulary";
import VocabularyForm from "@/components/elements/vocabularyForm";
import { getVocabularyById } from "@/api/vocabulary";

type paramsType = {
    language_id: string;
    lesson_id: string;
    voc_id: string;
};

export default async function UpdateVocabularyPage({ params }: { params: paramsType }) {
    const { lesson_id, voc_id } = await params;
    const vocabulary: Vocabulary = await getVocabularyById(voc_id);

    return (
        <main className="flex flex-col gap-4">
            <h1>Update Vocabulary</h1>
            <VocabularyForm vocabulary={vocabulary} lesson_id={lesson_id} />
        </main>
    );
}