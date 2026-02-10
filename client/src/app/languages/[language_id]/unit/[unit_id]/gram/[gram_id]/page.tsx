import { BASE_URL, getElementbyId } from "@/api";
import type Grammar from "@/interface/features/Grammar";
import Markdown from "react-markdown";
import remarkGfm from "remark-gfm";

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
                <Markdown remarkPlugins={[remarkGfm]}>{grammar.explanation}</Markdown>

                {grammar.learnable_sentences && grammar.learnable_sentences.length > 0 && (
                    <div>
                        <h3>Learnable Sentences:</h3>
                        <ul>
                            {grammar.learnable_sentences.map((sentence, index) => (
                                <li key={index}>
                                    {sentence.image_files && sentence.image_files.length > 0 && <img
                                        src={BASE_URL + sentence.image_files?.[0]}
                                        alt={sentence.text}
                                        width={200}
                                        height={200}
                                        />}
                                    {sentence.audio_files && sentence.audio_files.length > 0 && <audio
                                        src={BASE_URL + sentence.audio_files?.[0]}
                                        controls
                                        />}
                                    <p>{sentence.text}{sentence.translation && ` (${sentence.translation})`}</p>
                                </li>
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
                <DeleteButton element_id={grammar.id!}>
                    Delete Grammar
                </DeleteButton>
            </nav>
        </main>
    );
}