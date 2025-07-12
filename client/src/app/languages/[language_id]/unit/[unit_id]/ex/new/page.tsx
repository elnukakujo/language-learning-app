import CreateExerciseForm from "@/components/forms/createForms/createExerciseForm";

export default async function createExercisePage({ params }: { params: { unit_id: string } }) {
    const { unit_id } = await params;

    return (
        <div className="flex flex-col items-center justify-center h-full">
            <h1 className="text-2xl font-bold mb-4">Create New Exercise</h1>
            <CreateExerciseForm unit_id={unit_id} />
        </div>
    );
}