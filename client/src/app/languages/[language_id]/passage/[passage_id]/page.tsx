import { getPassageById } from "@/api/passage";
import type Passage from "@/interface/components/Passage";
import type Word from "@/interface/components/Word";
import type Character from "@/interface/components/Character";
import SentenceCard from "@/components/cards/componentCards/sentenceCard";
import RelatedCard from "@/components/cards/relatedCard";
import ElementPerformanceCard from "@/components/cards/elementCards/elementPerformanceCard";
import ElementSourcesCard from "@/components/cards/elementCards/elementSourcesCard";
import ElementTagsCard from "@/components/cards/elementCards/elementTagsCard";
import DeleteButton from "@/components/buttons/deleteButton";

export default async function PassagePage({
  params,
}: {
  params: { language_id: string; passage_id: string };
}) {
  const { passage_id } = await params;
  const passage = (await getPassageById(passage_id)) as Passage & {
    words?: Partial<Word>[];
    characters?: Partial<Character>[];
  };

  return (
    <main>
      <article className="flex flex-col space-y-4">
        <h1>Passage Sheet</h1>
        <SentenceCard sentence={passage} />

        <RelatedCard
          languageId={params.language_id}
          words={passage.words}
          characters={passage.characters}
        />

        <ElementTagsCard element={passage} />
        <ElementSourcesCard element={passage} />
        <ElementPerformanceCard element={passage} />
      </article>
      <nav className="flex flex-row space-x-4">
        <DeleteButton element_id={passage.id!}>Delete Passage</DeleteButton>
      </nav>
    </main>
  );
}
