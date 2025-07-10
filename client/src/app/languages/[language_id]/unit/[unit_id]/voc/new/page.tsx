import CreateVocabularyForm from "@/components/forms/createForms/createVocabularyForm";

export default function createVocabularyPage({ params }: { params: { unit_id: string } }) {
    const { unit_id } = params;

    return (
        <div className="flex flex-col items-center justify-center h-full">
            <h1 className="text-2xl font-bold mb-4">Create New Vocabulary</h1>
            <CreateVocabularyForm unit_id={unit_id} />
        </div>
    );
}