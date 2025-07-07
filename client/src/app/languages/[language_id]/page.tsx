import { getLanguageData } from "@/api";

import UnitOverviewCard from "@/components/cards/unitOverviewCard";

type Unit = {
    id: string;
    title: string;
    description: string;
    score: number;
    last_seen: Date;
};

export default async function Language({ params }: { params: { language_id: string } }) {
    const { language_id } = await params;
    const { language, units } = await getLanguageData(language_id);

    return (
        <main>
            <header>
                <h1>{language.flag} {language.name} ({language.native_name})</h1>
                <p>Language Level: {language.level}</p>
                <p>Language Score: {language.score.toFixed(1)}/100</p>
                <p>Last Seen: {new Date(language.last_seen).toLocaleDateString()}</p>
                {language.current_unit_id && <p>Current Unit ID: {language.current_unit_id}</p>}
            </header>
            <article>
                <h2>Units</h2>
                <ul>
                    {units.map((unit: Unit) => (
                        <li key={unit.id}>
                            <UnitOverviewCard unit={unit} />
                        </li>
                    ))}
                </ul>
            </article>
        </main>
    );
}