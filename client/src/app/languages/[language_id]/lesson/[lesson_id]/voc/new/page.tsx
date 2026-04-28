import VocabularyForm from "@/components/forms/entityForms/vocabularyForm";

export default async function createVocabularyPage({ params }: { params: { lesson_id: string } }) {
    const { lesson_id } = await params;

    return (
        <div className="flex flex-col items-center justify-center h-full">
            <h1 className="text-2xl font-bold mb-4">Create New Vocabulary</h1>
            <VocabularyForm lesson_id={lesson_id} />
        </div>
    );
}