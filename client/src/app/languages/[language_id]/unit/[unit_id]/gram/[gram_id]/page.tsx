import { getElementbyId } from "@/api";
import type Grammar from "@/interface/Grammar";
import Markdown from "react-markdown";

export default async function GrammarPage({ params }: { params: { language_id: string, unit_id: string, gram_id: string } }) {
    const { gram_id } = await params;
    const grammar: Grammar = await getElementbyId(gram_id);
    console.log(grammar);

    return (
        <main>
            <h1>{grammar.title}</h1>
            <Markdown>{grammar.explanation}</Markdown>
            <p>Score: {grammar.score.toFixed(1)}/100</p>
            <p>Last seen: {new Date(grammar.last_seen).toLocaleDateString('en-US')}</p>
        </main>
    );
}