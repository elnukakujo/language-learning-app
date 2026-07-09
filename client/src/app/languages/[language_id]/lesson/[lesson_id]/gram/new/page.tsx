import GrammarForm from "@/components/elements/grammarForm";

export default async function createGrammarPage({ params }: { params: { lesson_id: string } }) {
    const { lesson_id } = await params;

    return (
        <main className="flex flex-col gap-4">
            <h1>Create New Grammar</h1>
            <GrammarForm lesson_id={lesson_id} />
        </main>
    );
}