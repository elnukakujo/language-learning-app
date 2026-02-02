import { getElementbyId } from "@/api";
import DeleteButton from "@/components/buttons/deleteButton";
import NavButton from "@/components/buttons/navButton";
import type Vocabulary from "@/interface/features/Vocabulary";

export default async function VocabularyPage({ params }: { params: { language_id: string, unit_id: string, voc_id: string } }) {
    const { voc_id, unit_id, language_id } = await params;
    const vocabulary: Vocabulary = await getElementbyId(voc_id);

    return (
        <main>
            <article>    
                <h1>{vocabulary.word.word} {vocabulary.word.phonetic && <span>({vocabulary.word.phonetic})</span>} {vocabulary.word.translation}</h1>
                {vocabulary.example_sentences && vocabulary.example_sentences[0] && (
                    <p>Example sentence: {vocabulary.example_sentences[0].text}</p>
                )}
                <p>Type: {vocabulary.word.type || "N/A"}</p>
                <p>Score: {vocabulary.score?.toFixed(1)}/100</p>
                <p>Last seen: {new Date(vocabulary.last_seen || 0).toLocaleDateString('en-US')}</p>
            </article>
            <nav className="flex flex-row space-x-4">
                <NavButton path={`/languages/${language_id}/unit/${unit_id}/voc/${voc_id}/update`}>
                    Update the informations
                </NavButton>
                <DeleteButton element_id={vocabulary.id} />
            </nav>
        </main>
    );
}
