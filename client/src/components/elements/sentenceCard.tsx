import Passage from "@/interface/components/Word";
import ElementMediaCard from "./elementMediaCard";

export default function SentenceCard({ sentence, hiddenTranslation }: { sentence: Passage | Partial<Passage>; hiddenTranslation?: boolean }) {
    const hasMedia = (sentence.image_files && sentence.image_files.length > 0) || (sentence.audio_files && sentence.audio_files.length > 0);
    return (
        <section className="card">
            <h2 className="mb-1 text-lg font-semibold">Sentence</h2>
            
            <div className="index-divider pt-3 flex flex-col space-y-4">
                {/* ── Main sentence row ──────────────────────────────────────────── */}
                <div className="flex flex-wrap items-baseline gap-2">
                    <span className="font-serif text-2xl font-semibold text-foreground">
                        {sentence.text!}
                    </span>
                    {!hiddenTranslation && sentence.translation && (
                        <span className="font-mono text-sm text-muted">{sentence.translation}</span>
                    )}
                </div>

                {hasMedia && <ElementMediaCard element={sentence} />}
            </div>
        </section>
    );
}