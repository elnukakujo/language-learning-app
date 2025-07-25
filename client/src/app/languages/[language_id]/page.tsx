import { getLanguageData } from "@/api";

import UnitOverviewCard from "@/components/cards/unitOverviewCard";
import type Unit from "@/interface/Unit";
import NavButton from "@/components/buttons/navButton";
import DeleteButton from "@/components/buttons/deleteButton";

export default async function Language({ params }: { params: { language_id: string } }) {
    const { language_id } = await params;
    const { language, units } = await getLanguageData(language_id);
    const hasUnits = units && units.length > 0;

    return (
        <main>
            <header>
                <h1>{language.flag} {language.name} ({language.native_name})</h1>
                {language.level && <p>Language Level: {language.level}</p>}
                <p>Language Score: {language.score.toFixed(1)}/100</p>
                <p>Last Seen: {new Date(language.last_seen).toLocaleDateString()}</p>
                {language.current_unit_id && <p>Current Unit ID: {language.current_unit_id}</p>}
                <nav>
                    <NavButton path={`/languages/${language_id}/update`}>
                        <p>Update Language</p>
                    </NavButton>
                    <DeleteButton element_id={language_id}/>
                </nav>
            </header>
            <article>
                {
                    hasUnits && 
                    (
                        <section>
                            <h2>Units</h2>
                            <ul>
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