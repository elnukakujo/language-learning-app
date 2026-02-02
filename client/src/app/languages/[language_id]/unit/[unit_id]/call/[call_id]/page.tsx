import { getElementbyId } from "@/api";
import type Character from "@/interface/features/Calligraphy";
import Markdown from "react-markdown";

import NavButton from "@/components/buttons/navButton";
import DeleteButton from "@/components/buttons/deleteButton";

type paramsType = {
    language_id: string;
    unit_id: string;
    call_id: string;
};

export default async function CalligraphyPage({ params }: { params: paramsType }) {
    const { call_id, language_id, unit_id } = await params;
    const calligraphy: Character = await getElementbyId(call_id);
    const updatePath = `/languages/${language_id}/unit/${unit_id}/call/${call_id}/update`;

    return (
        <main>
            <article>    
                <h1>{calligraphy.character.character} {calligraphy.character.phonetic && <span>({calligraphy.character.phonetic})</span>} {calligraphy.character.meaning}</h1>
                {calligraphy.character.radical && <p>Radical: {calligraphy.character.radical}</p>}
                {calligraphy.example_word && (
                    <p>Example word: {calligraphy.example_word.word}</p>
                )}
                <p>Score: {calligraphy.score?.toFixed(1)}/100</p>
                <p>Last seen: {new Date(calligraphy.last_seen || 0).toLocaleDateString('en-US')}</p>
            </article>
            <nav className="flex flex-row space-x-4">
                <NavButton path={`/languages/${language_id}/unit/${unit_id}/call/${call_id}/update`}>
                    Update the informations
                </NavButton>
                <DeleteButton element_id={calligraphy.id!} />
            </nav>
        </main>
    );
}