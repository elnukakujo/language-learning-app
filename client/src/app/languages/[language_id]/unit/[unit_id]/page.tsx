import { getUnitData } from "@/api";
import VocabularyList from "@/components/lists/vocabularyList";
import GrammarList from "@/components/lists/grammarList";
import CharacterList from "@/components/lists/characterList";
import ExerciseList from "@/components/lists/exerciseList";

import type Unit from "@/interface/Unit";

import NavButton from "@/components/buttons/navButton";
import DeleteButton from "@/components/buttons/deleteButton";

interface ExtendedUnit extends Unit {
    vocabulary: {
        items: Array<{
            id: string;
            word: string;
            translation: string;
            score: number;
        }>;
        count: number;
    };
    grammar: {
        items: Array<{
            id: string;
            title: string;
            score: number;
        }>;
        count: number;
    };
    characters: {
        items: Array<{
            id: string;
            character: string;
            meaning: string;
            score: number;
        }>;
        count: number;
    };
    exercises: {
        items: Array<{
            type: string;
            count: number;
            score: number;
        }>;
        count: number;
    };
}

export default async function Unit({ params }: { params: { language_id: string, unit_id: string } }) {
    const { language_id, unit_id } = await params;
    const unit: ExtendedUnit = await getUnitData(unit_id);

    return (
        <main>
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
                <VocabularyList vocProps={unit.vocabulary} />
                <GrammarList gramProps={unit.grammar} />
                <CharacterList charProps={unit.characters} />
                <ExerciseList exProps={unit.exercises} />
            </article>
        </main>
    );
}
