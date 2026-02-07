import CreateCalligraphyForm from "@/components/forms/createForms/createCalligraphyForm";

export default async function createCalligraphyPage({ params }: { params: { unit_id: string } }) {
    const { unit_id } = await params;

    return (
        <div className="flex flex-col items-center justify-center h-full">
            <h1 className="text-2xl font-bold mb-4">Create New Calligraphy</h1>
            <CreateCalligraphyForm unit_id={unit_id} />
        </div>
    );
}