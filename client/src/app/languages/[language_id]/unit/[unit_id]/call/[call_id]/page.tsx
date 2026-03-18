import Image from "next/image";

import { BASE_URL, getElementbyId } from "@/api";
import type Character from "@/interface/features/Calligraphy";
import NavButton from "@/components/buttons/navButton";
import DeleteButton from "@/components/buttons/deleteButton";

type paramsType = {
    language_id: string;
    unit_id: string;
    call_id: string;
};

export default async function CalligraphyPage({ params }: { params: paramsType }) {
    const { call_id, language_id, unit_id } = await params;
    const calligraphy: Character = await getElementbyId(call_id);

    return (
        <main>
            <article className="flex flex-col space-y-4">
                <h1>Calligraphy Sheet</h1>
                <section>
                    <h3>Character Information</h3>
                    <p>{calligraphy.character.character} {calligraphy.character.phonetic && `(${calligraphy.character.phonetic})`} {calligraphy.character.meaning}</p>
                    {calligraphy.character.radical && <p>Radical: {calligraphy.character.radical}</p>}
                    {calligraphy.character.strokes && <p>Strokes: {calligraphy.character.strokes}</p>}
                </section>
                {calligraphy.character.image_files && calligraphy.character.image_files.length > 0 && (
                    <section className="flex flex-row space-x-4 items-center">
                        {calligraphy.character.image_files.map((url, index) => (
                            <Image
                                key={index}
                                src={BASE_URL + url}
                                alt={calligraphy.character.character}
                                width={200}
                                height={200}
                            />
                        ))}
                    </section>
                )}
                {calligraphy.character.audio_files && calligraphy.character.audio_files.length > 0 && (
                    <section className="flex flex-col space-y-4 items-baseline" >
                        {calligraphy.character.audio_files.map((url, index) => (
                            <audio
                                key={index}
                                src={BASE_URL + url}
                                controls
                        />
                        ))}
                    </section>
                )}
                
                {calligraphy.example_word && (
                    <section className="flex flex-col space-y-4 items-baseline">
                        <h3>Example Word</h3>
                        <article
                            className="flex flex-col space-y-2 items-baseline"
                        >
                            <section>
                                <p>{calligraphy.example_word.word}</p>
                                {calligraphy.example_word.translation && <p>Sentence Translation: {calligraphy.example_word.translation}</p>}
                            </section>
                            {calligraphy.example_word.image_files!.length > 0 && (
                                <section className="flex flex-row space-x-4 items-center">
                                    {calligraphy.example_word.image_files!.map((url, index) => (
                                        <Image
                                            key={index}
                                            src={BASE_URL + url}
                                            alt={calligraphy.example_word!.word}
                                            width={200}
                                            height={200}
                                        />
                                    ))}
                                </section>
                            )}
                            {calligraphy.example_word.audio_files!.length > 0 && (
                                <section className="flex flex-col space-y-4 items-baseline">
                                    {calligraphy.example_word.audio_files!.map((url, index) => (
                                        <audio
                                            key={index}
                                            src={BASE_URL + url}
                                            controls
                                        />
                                    ))}
                                </section>
                            )}
                        </article>
                    </section>
                )}
                <section>
                    <h3>Performance Information</h3>
                    <p>Score: {calligraphy.score?.toFixed(1)}/100</p>
                    <p>Last seen: {new Date(calligraphy.last_seen || 0).toLocaleDateString('en-US')}</p>
                </section>
            </article>
            <nav className="flex flex-row space-x-4">
                <NavButton path={`/languages/${language_id}/unit/${unit_id}/call/${call_id}/update`}>
                    Update the informations
                </NavButton>
                <DeleteButton element_id={calligraphy.id!} />
            </nav>
        </main>
    );
}