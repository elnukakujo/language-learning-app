import { getUnitData } from "@/api";
import UnitList from "@/components/unitList";

import type Unit from "@/interface/Unit";

interface ExtendedUnit extends Unit {
    vocabulary?: {
        items: Array<{
            id: string;
            word: string;
            translation: string;
        }>;
        count: number;
    };
    grammar?: {
        items: Array<{
            id: string;
            title: string;
        }>;
        count: number;
    };
    characters?: {
        items: Array<{
            id: string;
            character: string;
            translation: string;
        }>;
        count: number;
    };
    exercises?: {
        items: Array<{
            type: string;
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
            <p>Score: {unit.score.toFixed(1)}/100</p>
            <article className="flex flex-row gap-8 justify-around">
                <UnitList type="v" props={unit.vocabulary} />
                <UnitList type="g" props={unit.grammar} />
                <UnitList type="c" props={unit.characters} />
                <section className="flex flex-col gap-4 w-[14rem]">
                    <h2>Exercises</h2>
                    {unit.exercises && <ul>
                        {unit.exercises.items.map((item, index) => (
                            <li key={index}>{item.type}</li>
                        ))}
                    </ul>
                    }
                </section>
            </article>
        </main>
    );
}
