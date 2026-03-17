import { BASE_URL, getElementbyId } from "@/api";
import DeleteButton from "@/components/buttons/deleteButton";
import NavButton from "@/components/buttons/navButton";
import type Vocabulary from "@/interface/features/Vocabulary";

export default async function VocabularyPage({ params }: { params: { language_id: string, unit_id: string, voc_id: string } }) {
    const { voc_id, unit_id, language_id } = await params;
    const vocabulary: Vocabulary = await getElementbyId(voc_id);

    return (
        <main>
            <article className="flex flex-col space-y-4">
                <h1>Vocabulary Sheet</h1>
                <section>
                    <h3>Word Information</h3>
                    <p>{vocabulary.word.word} {(vocabulary.word.phonetic || vocabulary.word.gender) && `(${[vocabulary.word.phonetic, vocabulary.word.gender].filter(v => v).join(', ')})`} {vocabulary.word.translation}</p>
                    <p>Type: {vocabulary.word.type || "N/A"}</p>
                </section>
                {vocabulary.word.image_files!.length > 0 && (
                    <section className="flex flex-row space-x-4 items-center">
                        {vocabulary.word.image_files!.map((url, index) => (
                            <img
                                key={index}
                                src={BASE_URL + url}
                                alt={vocabulary.word.word}
                                width={200}
                                height={200}
                            />
                        ))}
                    </section>
                )}
                {vocabulary.word.audio_files!.length > 0 && (
                    <section className="flex flex-col space-y-4 items-baseline" >
                        {vocabulary.word.audio_files!.map((url, index) => (
                            <audio
                                key={index}
                                src={BASE_URL + url}
                                controls
                        />
                        ))}
                    </section>
                )}
                {vocabulary.example_sentences!.length > 0 && (
                    <section className="flex flex-col space-y-4 items-baseline">
                        <h3>Example Sentences</h3>
                        {vocabulary.example_sentences!.map((sentence, index) => (
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
                    <p>Score: {vocabulary.score?.toFixed(1)}/100</p>
                    <p>Last seen: {new Date(vocabulary.last_seen || 0).toLocaleDateString('en-US')}</p>
                </section>
            </article>
            <nav className="flex flex-row space-x-4">
                <NavButton path={`/languages/${language_id}/unit/${unit_id}/voc/${voc_id}/update`}>
                    Update the informations
                </NavButton>
                <DeleteButton element_id={vocabulary.id!} />
            </nav>
        </main>
    );
}
