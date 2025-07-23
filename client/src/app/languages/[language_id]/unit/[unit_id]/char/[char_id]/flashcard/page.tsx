import Character from "@/interface/Character";
import { getElementbyId, getNext } from "@/api";
import CharacterFlashCard from "@/components/cards/characterFlashCard";
import NavButton from "@/components/buttons/navButton";

export default async function CharacterFlashCardPage({ params }: { params: { language_id: string; unit_id: string; char_id: string }}) {
    const { language_id, unit_id, char_id } = await params;

    const character: Character = await getElementbyId(char_id);
    const next_char_id: string = await getNext(char_id);

    return (
        <main>
            <h1>Character Flashcard</h1>
            <CharacterFlashCard character={character} />
            <NavButton path={`/languages/${language_id}/unit/${unit_id}/char/${next_char_id}/flashcard`}>
                <p>Next Vocabulary</p>
            </NavButton>
        </main>
    );
}