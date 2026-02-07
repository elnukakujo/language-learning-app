import { getElementbyId, getLanguageData } from "@/api";
import type Vocabulary from "@/interface/features/Vocabulary";
import UpdateVocabularyForm from "@/components/forms/updateForms/updateVocabularyForm";

type paramsType = {
    language_id: string;
    unit_id: string;
    voc_id: string;
};

export default async function UpdateVocabularyPage({ params }: { params: paramsType }) {
    const { voc_id, language_id } = await params;
    const vocabulary: Vocabulary = await getElementbyId(voc_id);

    return (
        <main className="p-4">
            <h1 className="text-2xl font-semibold mb-4">Update Vocabulary</h1>
            <UpdateVocabularyForm vocabulary={vocabulary} />
        </main>
    );
}