import { getCharacterById } from "@/api/character";
import type Character from "@/interface/components/Character";
import type Word from "@/interface/components/Word";
import type Passage from "@/interface/components/Passage";
import CharacterCard from "@/components/cards/componentCards/characterCard";
import RelatedCard from "@/components/cards/relatedCard";
import ElementPerformanceCard from "@/components/cards/elementCards/elementPerformanceCard";
import ElementSourcesCard from "@/components/cards/elementCards/elementSourcesCard";
import ElementTagsCard from "@/components/cards/elementCards/elementTagsCard";
import DeleteButton from "@/components/buttons/deleteButton";

export default async function CharacterPage({
  params,
}: {
  params: { language_id: string; character_id: string };
}) {
  const { character_id, language_id } = await params;
  const character = (await getCharacterById(character_id)) as Character & {
    words?: Partial<Word>[];
    passages?: Partial<Passage>[];
  };

  return (
    <main>
      <article className="flex flex-col space-y-4">
        <h1>Character Sheet</h1>
        <CharacterCard character={character} />

        <RelatedCard
          languageId={language_id}
          words={character.words}
          passages={character.passages}
        />

        <ElementTagsCard element={character} />
        <ElementSourcesCard element={character} />
        <ElementPerformanceCard element={character} />
      </article>
      <nav className="flex flex-row space-x-4">
        <DeleteButton element_id={character.id!}>Delete Character</DeleteButton>
      </nav>
    </main>
  );
}
