import Character from "@/interface/components/Character";
import ElementMediaCard from "../elementCards/elementMediaCard";

export default function CharacterCard({ character, hiddenTranslation, hiddenAdditionalInformations }: { character: Character | Partial<Character>; hiddenTranslation?: boolean; hiddenAdditionalInformations?: boolean }) {
    return (
        <section className="flex flex-col space-y-4 p-4 border rounded-md">
            <h3>Character Information</h3>
            <p>
                {character.character} {character.phonetic && ((hiddenTranslation && hiddenAdditionalInformations) || !hiddenTranslation) && `(${character.phonetic})`} {!hiddenTranslation && character.meaning}
            </p>
            {((hiddenTranslation && hiddenAdditionalInformations) || !hiddenTranslation) && (
                <>
                    {character.radical && <p>Radical: {character.radical}</p>}
                    {character.strokes && <p>Strokes: {character.strokes}</p>}
                    {(character.image_files && character.image_files.length > 0) || (character.audio_files && character.audio_files.length > 0) ? (
                        <ElementMediaCard element={character} />
                    ) : null}
                </>
            )}
        </section>
    );
}