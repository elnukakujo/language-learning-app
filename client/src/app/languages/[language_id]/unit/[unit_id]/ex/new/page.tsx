import CreateExerciseForm from "@/components/forms/createForms/createExerciseForm";
import { getCalligraphyByUnit, getGrammarByUnit, getVocabularyByUnit } from "@/api";
import Calligraphy from "@/interface/features/Calligraphy";
import Grammar from "@/interface/features/Grammar";
import Vocabulary from "@/interface/features/Vocabulary";

interface UnitElements {
    vocabularies: Vocabulary[];
    grammars: Grammar[];
    calligraphies: Calligraphy[];
}

export default async function createExercisePage({ params }: { params: { unit_id: string } }) {
    const { unit_id } = await params;

    const calligraphies: Calligraphy[] = await getCalligraphyByUnit(unit_id);
    const grammars: Grammar[] = await getGrammarByUnit(unit_id);
    const vocabularies: Vocabulary[] = await getVocabularyByUnit(unit_id);

    const unitElements: UnitElements = {
        vocabularies,
        grammars,
        calligraphies
    };

    return (
        <div className="flex flex-col items-center justify-center h-full">
            <h1 className="text-2xl font-bold mb-4">Create New Exercise</h1>
            <CreateExerciseForm unit_id={unit_id} unitElements={unitElements} />
        </div>
    );
}