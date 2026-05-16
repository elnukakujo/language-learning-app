import Grammar from "@/interface/features/Grammar";
import ElementMediaCard from "./elementCards/elementMediaCard";
import Markdown from "react-markdown";
import remarkGfm from "remark-gfm";

export default function GrammarCard({ grammar }: { grammar: Grammar | Partial<Grammar> }) {
    return (
        <section className="flex flex-col space-y-4 p-4 border rounded-md">
            <h3>Grammar Information</h3>
            <h4>{grammar.title}</h4>
            {grammar.explanation && <Markdown remarkPlugins={[remarkGfm]}>{grammar.explanation}</Markdown>}
            {(grammar.image_files && grammar.image_files.length > 0) || (grammar.audio_files && grammar.audio_files.length > 0) ? (
                <ElementMediaCard element={grammar} />
            ) : null}
        </section>
    );
}