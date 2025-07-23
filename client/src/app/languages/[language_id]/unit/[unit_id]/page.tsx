import { getUnitData } from "@/api";
import VocabularyList from "@/components/lists/vocabularyList";
import GrammarList from "@/components/lists/grammarList";
import CharacterList from "@/components/lists/characterList";
import ExerciseList from "@/components/lists/exerciseList";

import type Unit from "@/interface/Unit";

interface ExtendedUnit extends Unit {
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
    exercises: {
        items: Array<{
            type: string;
            count: number;
        }>;
        count: number;
    };
}

export default async function Unit({ params }: { params: { language_id: string, unit_id: string } }) {
    const { unit_id } = await params;
    const unit: ExtendedUnit = await getUnitData(unit_id);

    return (
        <main>
            <h1>{unit.title}</h1>
            <p>{unit.description}</p>
            <p>Score: {unit.score?.toFixed(1) || "N/A"}/100</p>
            <p>Last Seen: {new Date(unit.last_seen || 0).toLocaleDateString('en-US')}</p>
            <article className="flex flex-row gap-8 justify-around">
                <VocabularyList vocProps={unit.vocabulary} />
                <GrammarList gramProps={unit.grammar} />
                <CharacterList charProps={unit.characters} />
                <ExerciseList exProps={unit.exercises} />
            </article>
        </main>
    );
}
