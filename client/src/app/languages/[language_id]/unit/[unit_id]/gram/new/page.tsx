import CreateGrammarForm from "@/components/forms/createForms/createGrammarForm";

export default async function createGrammarPage({ params }: { params: { unit_id: string } }) {
    const { unit_id } = await params;

    return (
        <div className="flex flex-col items-center">
            <h1 className="text-2xl font-bold mb-4">Create New Grammar</h1>
            <CreateGrammarForm unit_id={unit_id} />
        </div>
    );
}