import { getWordById } from "@/api/word";
import type Word from "@/interface/components/Word";
import type Character from "@/interface/components/Character";
import type Passage from "@/interface/components/Passage";
import WordCard from "@/components/cards/componentCards/wordCard";
import RelatedCard from "@/components/cards/relatedCard";
import ElementPerformanceCard from "@/components/cards/elementCards/elementPerformanceCard";
import ElementSourcesCard from "@/components/cards/elementCards/elementSourcesCard";
import ElementTagsCard from "@/components/cards/elementCards/elementTagsCard";
import DeleteButton from "@/components/buttons/deleteButton";

export default async function WordPage({
  params,
}: {
  params: { language_id: string; word_id: string };
}) {
  const { word_id, language_id } = await params;
  const word = (await getWordById(word_id)) as Word & {
    characters?: Partial<Character>[];
    passages?: Partial<Passage>[];
  };

  return (
    <main>
      <article className="flex flex-col space-y-4">
        <h1>Word Sheet</h1>
        <WordCard word={word} />

        <RelatedCard
          languageId={language_id}
          characters={word.characters}
          passages={word.passages}
        />

        <ElementTagsCard element={word} />
        <ElementSourcesCard element={word} />
        <ElementPerformanceCard element={word} />
      </article>
      <nav className="flex flex-row space-x-4">
        <DeleteButton element_id={word.id!}>Delete Word</DeleteButton>
      </nav>
    </main>
  );
}
