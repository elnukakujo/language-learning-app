import { getLanguageData } from "@/api";

import UnitOverviewCard from "@/components/cards/unitOverviewCard";
import type Unit from "@/interface/containers/Unit";
import NavButton from "@/components/buttons/navButton";
import DeleteButton from "@/components/buttons/deleteButton";

export default async function Language({ params }: { params: { language_id: string } }) {
    const { language_id } = await params;
    const { language, units } = await getLanguageData(language_id);
    const hasUnits = units && units.length > 0;

    return (
        <main className="flex flex-col space-y-4">
            <header className="flex flex-col">
                <h1>{language.flag} {language.name} ({language.native_name})</h1>
                {language.level && <p>Language Level: {language.level}</p>}
                <p>Language Score: {language.score.toFixed(1)}/100</p>
                <p>Last Seen: {new Date(language.last_seen).toLocaleDateString()}</p>
                {language.current_unit && <p>Current Unit ID: {language.current_unit}</p>}
                <nav className="flex flex-row space-x-4">
                    {language.current_unit && <NavButton path={`/languages/${language_id}/unit/${language.current_unit}`}>
                        <p>Go to Current Unit</p>
                    </NavButton>}
                    <NavButton path={`/languages/${language_id}/update`}>
                        <p>Update Language</p>
                    </NavButton>
                    <DeleteButton element_id={language_id}/>
                </nav>
            </header>
            <article className="flex flex-col space-y-4">
                {
                    hasUnits && 
                    (
                        <section>
                            <h2>Units</h2>
                            <ul className="flex flex-col space-y-2">
                                {units.map((unit: Unit) => (
                                    <li key={unit.id}>
                                        <UnitOverviewCard unit={unit} />
                                    </li>
                                ))}
                            </ul>
                        </section>
                    )
                }
                
                <NavButton path={`/languages/${language_id}/unit/new`}>
                    <p>Create New Unit</p>
                </NavButton>
            </article>
        </main>
    );
}