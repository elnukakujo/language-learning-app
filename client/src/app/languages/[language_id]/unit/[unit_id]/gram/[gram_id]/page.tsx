import { getElementbyId } from "@/api";
import type Grammar from "@/interface/features/Grammar";
import Markdown from "react-markdown";

import NavButton from "@/components/buttons/navButton";
import DeleteButton from "@/components/buttons/deleteButton";

type paramsType = {
    language_id: string;
    unit_id: string;
    gram_id: string;
};

export default async function GrammarPage({ params }: { params: paramsType }) {
    const { gram_id, language_id, unit_id } = await params;
    const grammar: Grammar = await getElementbyId(gram_id);
    const updatePath = `/languages/${language_id}/unit/${unit_id}/gram/${gram_id}/update`;

    return (
        <main>
            <section>
                <h1>{grammar.title}</h1>
                <Markdown>{grammar.explanation}</Markdown>
                {grammar.learnable_sentences && grammar.learnable_sentences.length > 0 && (
                    <div>
                        <strong>Learnable Sentences:</strong>
                        <ul>
                            {grammar.learnable_sentences.map((sentence, index) => (
                                <li key={index}>{sentence.text}</li>
                            ))}
                        </ul>
                    </div>
                )}
                <p>Score: {grammar.score?.toFixed(1) || 0}/100</p>
                <p>Last seen: {new Date(grammar.last_seen || 0).toLocaleDateString('en-US')}</p>
            </section>
            <nav className="flex flex-row space-x-4">
                <NavButton path={`/languages/${language_id}/unit/${unit_id}/gram/${gram_id}/update`}>
                    Update the Grammar
                </NavButton>
                <DeleteButton element_id={grammar.id}>
                    Delete Grammar
                </DeleteButton>
            </nav>
        </main>
    );
}