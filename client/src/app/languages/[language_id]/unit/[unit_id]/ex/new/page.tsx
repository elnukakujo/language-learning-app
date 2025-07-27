import CreateExerciseForm from "@/components/forms/createForms/createExerciseForm";
import { getUnitData } from "@/api";

interface UnitElements {
    vocabulary: {
        items: Array<{
            id: string;
            word: string;
            translation: string;
        }>;
        count: number;
    };
    grammar: {
        items: Array<{
            id: string;
            title: string;
        }>;
        count: number;
    };
    characters: {
        items: Array<{
            id: string;
            character: string;
            meaning: string;
        }>;
        count: number;
    };
}

export default async function createExercisePage({ params }: { params: { unit_id: string } }) {
    const { unit_id } = await params;

    const unitElements: UnitElements = await getUnitData(unit_id);

    return (
        <div className="flex flex-col items-center justify-center h-full">
            <h1 className="text-2xl font-bold mb-4">Create New Exercise</h1>
            <CreateExerciseForm unit_id={unit_id} unitElements={unitElements} />
        </div>
    );
}