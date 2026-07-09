import VocabularyForm from "@/components/elements/vocabularyForm";

export default async function createVocabularyPage({ params }: { params: { lesson_id: string } }) {
    const { lesson_id } = await params;

    return (
        <main className="flex flex-col gap-4">
            <h1>Create New Vocabulary</h1>
            <VocabularyForm lesson_id={lesson_id} />
        </main>
    );
}