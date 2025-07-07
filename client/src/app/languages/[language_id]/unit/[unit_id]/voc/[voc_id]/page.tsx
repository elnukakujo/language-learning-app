import { getElementbyId } from "@/api";
import type Vocabulary from "@/interface/Vocabulary";

export default async function VocabularyPage({ params }: { params: { language_id: string, unit_id: string, voc_id: string } }) {
    const { voc_id } = await params;
    const vocabulary: Vocabulary = await getElementbyId(voc_id);

    return (
        <main>
            <h1>{vocabulary.word} {vocabulary.phonetic && <span>({vocabulary.phonetic})</span>} {vocabulary.translation}</h1>
            {vocabulary.example_sentence && (
                <p>Example sentence: {vocabulary.example_sentence}</p>
            )}
            <p>Type: {vocabulary.type || "N/A"}</p>
            <p>Score: {vocabulary.score.toFixed(1)}/100</p>
            <p>Last seen: {new Date(vocabulary.last_seen).toLocaleDateString('en-US')}</p>
        </main>
    );
}
