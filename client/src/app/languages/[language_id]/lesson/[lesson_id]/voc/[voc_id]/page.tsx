import { getElementbyId } from "@/api";
import DeleteButton from "@/components/buttons/deleteButton";
import NavButton from "@/components/buttons/navButton";
import type Vocabulary from "@/interface/features/Vocabulary";
import ElementPerformanceCard from "@/components/cards/elementCards/elementPerformanceCard";
import ElementSourcesCard from "@/components/cards/elementCards/elementSourcesCard";
import ElementTagsCard from "@/components/cards/elementCards/elementTagsCard";
import WordCard from "@/components/cards/componentCards/wordCard";
import SentenceCard from "@/components/cards/componentCards/sentenceCard";

export default async function VocabularyPage({ params }: { params: { language_id: string, lesson_id: string, voc_id: string } }) {
    const { voc_id, lesson_id, language_id } = await params;
    const vocabulary: Vocabulary = await getElementbyId(voc_id);
    console.log(vocabulary);
    return (
        <main>
            <article className="flex flex-col space-y-4">
                <h1>Vocabulary Sheet</h1>
                <WordCard word={vocabulary.word} />
                {vocabulary.example_sentences!.length > 0 && (
                    <section className="flex flex-col space-y-4 items-baseline">
                        <h3>Example Sentences</h3>
                        {vocabulary.example_sentences!.map((sentence, idx) => (
                            <SentenceCard key={idx} sentence={sentence} />
                        ))}
                    </section>
                )}
                <ElementTagsCard element={vocabulary} />
                <ElementSourcesCard element={vocabulary} />
                <ElementPerformanceCard element={vocabulary} />
            </article>
            <nav className="flex flex-row space-x-4">
                <NavButton path={`/languages/${language_id}/lesson/${lesson_id}/voc/${voc_id}/update`}>
                    Update the informations
                </NavButton>
                <DeleteButton element_id={vocabulary.id!} />
            </nav>
        </main>
    );
}
