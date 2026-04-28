import CalligraphyForm from "@/components/forms/entityForms/calligraphyForm";

export default async function createCalligraphyPage({ params }: { params: { lesson_id: string } }) {
    const { lesson_id } = await params;

    return (
        <div className="flex flex-col items-center justify-center h-full">
            <h1 className="text-2xl font-bold mb-4">Create New Calligraphy</h1>
            <CalligraphyForm lesson_id={lesson_id} />
        </div>
    );
}