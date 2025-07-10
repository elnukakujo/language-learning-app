import { getElementbyId } from "@/api";
import type Character from "@/interface/Character";
import Markdown from "react-markdown";

import NavButton from "@/components/buttons/navButton";
import DeleteButton from "@/components/buttons/deleteButton";

type paramsType = {
    language_id: string;
    unit_id: string;
    char_id: string;
};

export default async function CharacterPage({ params }: { params: paramsType }) {
    const { char_id, language_id, unit_id } = await params;
    const character: Character = await getElementbyId(char_id);
    const updatePath = `/languages/${language_id}/unit/${unit_id}/char/${char_id}/update`;

    return (
        <main>
            <article>    
                <h1>{character.character} {character.phonetic && <span>({character.phonetic})</span>} {character.meaning}</h1>
                <p>{character.components}</p>
                {character.example_word && (
                    <p>Example expression: {character.example_word}</p>
                )}
                <p>Score: {character.score.toFixed(1)}/100</p>
                <p>Last seen: {new Date(character.last_seen).toLocaleDateString('en-US')}</p>
            </article>
            <NavButton path={`/languages/${language_id}/unit/${unit_id}/char/${char_id}/update`}>
                Update the informations
            </NavButton>
            <DeleteButton element_id={character.id} />
        </main>
    );
}