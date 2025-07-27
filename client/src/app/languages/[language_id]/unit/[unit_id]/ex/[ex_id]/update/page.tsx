import { getElementbyId, getLanguageData, getUnitData } from "@/api";
import type Exercise from "@/interface/Exercise";
import UpdateExerciseForm from "@/components/forms/updateForms/updateExerciseForm";

type paramsType = {
    language_id: string;
    unit_id: string;
    ex_id: string;
};

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

export default async function UpdateExercisePage({ params }: { params: paramsType }) {
    const { language_id, unit_id, ex_id } = await params;
    const exercise: Exercise = await getElementbyId(ex_id);
    const languageInfo = await getLanguageData(language_id);
    const existingUnitsId: string[] = languageInfo.units.map((unit: { id: string }) => unit.id);

    const unitElements: UnitElements = await getUnitData(unit_id);

    return (
        <main className="p-4">
            <h1 className="text-2xl font-semibold mb-4">Update Exercise Informations</h1>
            <UpdateExerciseForm exercise={exercise} existingUnitsId={existingUnitsId} unitElements={unitElements} />
        </main>
    );
}