"use client";

import { useParams, useRouter } from "next/navigation";

type VocabularyProps = {
    items: Array<{
        id: string;
        word: string;
        translation: string;
    }>;
    count: number;
};

type GrammarProps = {
    items: Array<{
        id: string;
        title: string;
    }>;
    count: number;
};

type CharactersProps = {
    items: Array<{
        id: string;
        character: string;
        meaning: string;
    }>;
    count: number;
};

export default function UnitList({ type, props }: { type: string, props?: VocabularyProps | GrammarProps | CharactersProps }) {
    const { language_id, unit_id } = useParams<{ language_id: string, unit_id: string }>();

    let title:string;
    let path:string;
    switch (type) {
        case "v":
            title = "Vocabulary";
            path = "voc";
            break;
        case "g":
            title = "Grammar";
            path = "gram";
            break;
        case "c":
            title = "Characters";
            path = "char";
            break;
        default:
            throw new Error(`Unknown type: ${type}`);
    }

    const router = useRouter();
    const handleClick = (id: string) => {
        router.push(`/languages/${language_id}/unit/${unit_id}/${path}/${id}`);
    };
    return (
        <section className="flex flex-col gap-4 w-[14rem]">
            <h2>{title}</h2>
            {props && <ul className="list-item pl-5 space-y-1">
                {props.items.map((item, index) => (
                    <li key={index}>
                        <button onClick={() => handleClick(item.id)}>
                            {type === "v" && (
                                <>
                                    {(item as VocabularyProps["items"][0]).word} –{" "}
                                    {(item as VocabularyProps["items"][0]).translation}
                                </>
                            )}
                            {type === "g" && (
                                <>
                                    {(item as GrammarProps["items"][0]).title}
                                </>
                            )}
                            {type === "c" && (
                                <>
                                    {(item as CharactersProps["items"][0]).character} –{" "}
                                    {(item as CharactersProps["items"][0]).meaning}
                                </>
                            )}
                        </button>
                    </li>
                ))}
            </ul>}
        </section>
    );
}