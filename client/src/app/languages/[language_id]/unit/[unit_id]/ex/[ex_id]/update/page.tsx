import { getElementbyId } from "@/api";
import type Exercise from "@/interface/Exercise";
import UpdateExerciseForm from "@/components/forms/updateForms/updateExerciseForm";

type paramsType = {
    language_id: string;
    unit_id: string;
    ex_id: string;
};

export default async function UpdateExercisePage({ params }: { params: paramsType }) {
    const { ex_id } = await params;
    const exercise: Exercise = await getElementbyId(ex_id);

    return (
        <main className="p-4">
            <h1 className="text-2xl font-semibold mb-4">Update Exercise Informations</h1>
            <UpdateExerciseForm exercise={exercise} />
        </main>
    );
}