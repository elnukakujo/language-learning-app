import CalligraphyForm from "@/components/elements/calligraphyForm";

export default async function createCalligraphyPage({ params }: { params: Promise<{ lesson_id: string }> }) {
    const { lesson_id } = await params;

    return (
        <main className="flex flex-col gap-4">
            <h1>Create New Calligraphy</h1>
            <CalligraphyForm lesson_id={lesson_id} />
        </main>
    );
}