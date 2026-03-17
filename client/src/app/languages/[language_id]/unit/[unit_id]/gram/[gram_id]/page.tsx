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

    return (
        <main>
            <article className="flex flex-col space-y-4">
                <h1>{grammar.title}</h1>
                <Markdown remarkPlugins={[remarkGfm]}>{grammar.explanation}</Markdown>

                {grammar.image_files!.length > 0 && (
                    <section className="flex flex-row space-x-4 items-center">
                        {grammar.image_files!.map((url, index) => (
                            <img
                                key={index}
                                src={BASE_URL + url}
                                alt={grammar.title}
                                width={200}
                                height={200}
                            />
                        ))}
                    </section>
                )}
                {grammar.audio_files!.length > 0 && (
                    <section className="flex flex-col space-y-4 items-baseline" >
                        {grammar.audio_files!.map((url, index) => (
                            <audio
                                key={index}
                                src={BASE_URL + url}
                                controls
                        />
                        ))}
                    </section>
                )}

                {grammar.learnable_sentences!.length > 0 && (
                    <section className="flex flex-col space-y-4 items-baseline">
                        <h3>Learnable Sentences</h3>
                        {grammar.learnable_sentences!.map((sentence, index) => (
                            <article
                                key={index}
                                className="flex flex-col space-y-2 items-baseline"
                            >
                                <section>
                                    <p>{sentence.text}</p>
                                    {sentence.translation && <p>Sentence Translation: {sentence.translation}</p>}
                                </section>
                                {sentence.image_files!.length > 0 && (
                                    <section className="flex flex-row space-x-4 items-center">
                                        {sentence.image_files!.map((url, index) => (
                                            <img
                                                key={index}
                                                src={BASE_URL + url}
                                                alt={sentence.text}
                                                width={200}
                                                height={200}
                                            />
                                        ))}
                                    </section>
                                )}
                                {sentence.audio_files!.length > 0 && (
                                    <section className="flex flex-col space-y-4 items-baseline">
                                        {sentence.audio_files!.map((url, index) => (
                                            <audio
                                                key={index}
                                                src={BASE_URL + url}
                                                controls
                                            />
                                        ))}
                                    </section>
                                )}
                            </article>
                        ))}
                    </section>
                )}
                <section>
                    <h3>Performance Information</h3>
                    <p>Score: {grammar.score!.toFixed(1)}/100</p>
                    <p>Last seen: {new Date(grammar.last_seen || 0).toLocaleDateString('en-US')}</p>
                </section>
            </article>
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