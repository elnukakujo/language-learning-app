import { getCalligraphyByUnit, getElementbyId, getGrammarByUnit, getLanguageData, getUnitData, getVocabularyByUnit } from "@/api";
import type Exercise from "@/interface/features/Exercise";
import UpdateExerciseForm from "@/components/forms/updateForms/updateExerciseForm";
import Calligraphy from "@/interface/features/Calligraphy";
import Grammar from "@/interface/features/Grammar";
import Vocabulary from "@/interface/features/Vocabulary";

type paramsType = {
    language_id: string;
    unit_id: string;
    ex_id: string;
};

interface UnitElements {
    vocabularies: Vocabulary[];
    grammars: Grammar[];
    calligraphies: Calligraphy[];
}

export default async function UpdateExercisePage({ params }: { params: paramsType }) {
    const { language_id, unit_id, ex_id } = await params;
    const exercise: Exercise = await getElementbyId(ex_id);

    const calligraphies: Calligraphy[] = await getCalligraphyByUnit(unit_id);
    const grammars: Grammar[] = await getGrammarByUnit(unit_id);
    const vocabularies: Vocabulary[] = await getVocabularyByUnit(unit_id);

    const unitElements: UnitElements = {
        calligraphies,
        grammars,
        vocabularies
    };

    return (
        <main className="p-4">
            <h1 className="text-2xl font-semibold mb-4">Update Exercise Informations</h1>
            <UpdateExerciseForm exercise={exercise} unitElements={unitElements} />
        </main>
    );
}