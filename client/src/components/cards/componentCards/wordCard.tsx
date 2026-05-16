import Word from "@/interface/components/Word";
import ElementMediaCard from "../elementCards/elementMediaCard";

export default function WordCard({ word, hiddenTranslation, hiddenAdditionalInformations }: { word: Word | Partial<Word>; hiddenTranslation?: boolean; hiddenAdditionalInformations?: boolean }) {
    return (
        <section className="flex flex-col space-y-4 p-4 border rounded-md">
            <h4>Word Information</h4>
            <p>
                {word.word} {word.phonetic && ((hiddenTranslation && hiddenAdditionalInformations) || !hiddenTranslation) && `(${word.phonetic})`} {!hiddenTranslation && word.translation}
            </p>
            {((hiddenTranslation && hiddenAdditionalInformations) || !hiddenTranslation) && (
                <>
                    {word.word_type && <p>Type: {word.word_type}</p>}
                    {word.word_gender && <p>Gender: {word.word_gender}</p>}
                    {(word.image_files && word.image_files.length > 0) || (word.audio_files && word.audio_files.length > 0) ? (
                        <ElementMediaCard element={word} />
                    ) : null}
                </>
            )}
        </section>
    );
}