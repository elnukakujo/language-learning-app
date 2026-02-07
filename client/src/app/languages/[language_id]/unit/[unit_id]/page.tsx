import { getUnitData, getVocabularyByUnit, getGrammarByUnit, getCalligraphyByUnit, getExercisesByUnit } from "@/api";
import VocabularyList from "@/components/lists/vocabularyList";
import GrammarList from "@/components/lists/grammarList";
import CalligraphyList from "@/components/lists/characterList";
import ExerciseList from "@/components/lists/exerciseList";

import type Unit from "@/interface/containers/Unit";
import type Vocabulary from "@/interface/features/Vocabulary";
import type Grammar from "@/interface/features/Grammar";
import type Calligraphy from "@/interface/features/Calligraphy";
import type Exercise from "@/interface/features/Exercise";

import NavButton from "@/components/buttons/navButton";
import DeleteButton from "@/components/buttons/deleteButton";

export default async function Unit({ params }: { params: { language_id: string, unit_id: string } }) {
    const { language_id, unit_id } = await params;
    const unit: Unit = await getUnitData(unit_id);

    const vocabularies: Vocabulary[] = await getVocabularyByUnit(unit_id);
    const grammars: Grammar[] = await getGrammarByUnit(unit_id);
    const calligraphies: Calligraphy[] =  await getCalligraphyByUnit(unit_id);
    const exercises: Exercise[] = await getExercisesByUnit(unit_id);

    return (
        <main className="flex flex-col gap-8">
            <header>
                <h1>{unit.title}</h1>
                <p>{unit.description}</p>
                <p>Score: {unit.score?.toFixed(1) || "N/A"}/100</p>
                <p>Last Seen: {new Date(unit.last_seen || 0).toLocaleDateString('en-US')}</p>
                <nav className="flex flex-row space-x-4">
                    <NavButton path={`/languages/${language_id}/unit/${unit_id}/update`}>
                        <p>Update this Unit Informations</p>
                    </NavButton>
                    <DeleteButton element_id={unit_id}>
                        <p>Delete this Unit</p>
                    </DeleteButton>
                </nav>
            </header>
            <article className="flex flex-row gap-8 justify-around">
                <VocabularyList vocProps={vocabularies} />
                <GrammarList gramProps={grammars} />
                <CalligraphyList callProps={calligraphies} />
                <ExerciseList exProps={exercises} />
            </article>
        </main>
    );
}
