import Character from "@/interface/components/Character";
import ElementMediaCard from "./elementMediaCard";

export default function CharacterCard({ character, hiddenTranslation, hiddenAdditionalInformations }: { character: Character | Partial<Character>; hiddenTranslation?: boolean; hiddenAdditionalInformations?: boolean }) {
    return (
        <section className="card flex flex-col space-y-4">
            <h3>Character Information</h3>
            <div className="index-divider pt-3 flex flex-col space-y-4">
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
            </div>
        </section>
    );
}