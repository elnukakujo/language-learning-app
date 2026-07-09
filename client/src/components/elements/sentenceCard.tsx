import Passage from "@/interface/components/Word";
import ElementMediaCard from "./elementMediaCard";

export default function SentenceCard({ sentence, hiddenTranslation }: { sentence: Passage | Partial<Passage>; hiddenTranslation?: boolean }) {
    return (
        <section className="card flex flex-col space-y-4">
            <h4>Sentence Information</h4>
            <div className="index-divider pt-3 flex flex-col space-y-4">
                <p>{sentence.text} {sentence.translation && !hiddenTranslation && `(${sentence.translation})`}</p>
                {(sentence.image_files && sentence.image_files.length > 0) || (sentence.audio_files && sentence.audio_files.length > 0) ? (
                    <ElementMediaCard element={sentence} />
                ) : null}
            </div>
        </section>
    );
}