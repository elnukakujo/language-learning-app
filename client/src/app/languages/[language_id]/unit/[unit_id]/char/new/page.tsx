import CreateCharacterForm from "@/components/forms/createForms/createCharacterForm";

export default async function createCharacterPage({ params }: { params: { unit_id: string } }) {
    const { unit_id } = await params;

    return (
        <div className="flex flex-col items-center justify-center h-full">
            <h1 className="text-2xl font-bold mb-4">Create New Character</h1>
            <CreateCharacterForm unit_id={unit_id} />
        </div>
    );
}