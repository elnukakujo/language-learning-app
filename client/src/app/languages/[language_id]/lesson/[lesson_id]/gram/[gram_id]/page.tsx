import type Grammar from "@/interface/features/Grammar";

import NavButton from "@/components/layout/navButton";
import DeleteButton from "@/components/ui/buttons/deleteButton";
import ElementPerformanceCard from "@/components/elements/elementPerformanceCard";
import ElementSourcesCard from "@/components/elements/elementSourcesCard";
import ElementTagsCard from "@/components/elements/elementTagsCard";
import SentenceCard from "@/components/elements/sentenceCard";
import GrammarCard from "@/components/elements/grammarCard";
import { getGrammarById } from "@/api/grammar";

type paramsType = {
    language_id: string;
    lesson_id: string;
    gram_id: string;
};

export default async function GrammarPage({ params }: { params: Promise<paramsType> }) {
    const { gram_id, language_id, lesson_id } = await params;
    const grammar: Grammar = await getGrammarById(gram_id);

    return (
        <main>
            <article className="flex flex-col space-y-4">
                <h1>Grammar Sheet</h1>
                <GrammarCard grammar={grammar} />
                {grammar.example_sentences!.length > 0 && (
                    <section className="flex flex-col space-y-4 items-baseline">
                        <h3>Example Sentences</h3>
                        {grammar.example_sentences!.map((sentence, idx) => (
                            <SentenceCard key={idx} sentence={sentence} />
                        ))}
                    </section>
                )}
                <ElementTagsCard element={grammar} />
                <ElementSourcesCard element={grammar} />
                <ElementPerformanceCard element={grammar} />
            </article>
            <nav className="flex flex-row space-x-4">
                <NavButton path={`/languages/${language_id}/lesson/${lesson_id}/gram/${gram_id}/update`}>
                    Update the Grammar
                </NavButton>
                <DeleteButton element_id={grammar.id!}>
                    Delete Grammar
                </DeleteButton>
            </nav>
        </main>
    );
}