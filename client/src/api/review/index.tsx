import { BASE_URL } from "..";
import type Vocabulary from "@/interface/features/Vocabulary";
import type Grammar from "@/interface/features/Grammar";
import type Calligraphy from "@/interface/features/Calligraphy";

export type ReviewCard = Vocabulary | Grammar | Calligraphy;

export async function getReviewCards(languageId: string): Promise<ReviewCard[]> {
  const res = await fetch(`${BASE_URL}/api/review/${languageId}`);
  if (!res.ok) throw new Error(`Failed to fetch review cards for language ${languageId}`);
  return res.json();
}
