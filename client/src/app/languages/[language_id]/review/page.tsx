import ReviewFlashCard from "@/components/elements/reviewFlashCard";
import { getReviewCards } from "@/api/review";

export default async function ReviewPage({ params }: { params: Promise<{ language_id: string }> }) {
    const { language_id } = await params;
    const cards = await getReviewCards(language_id);

    return (
        <main>
            <h1>Daily Review</h1>
            <ReviewFlashCard cards={cards} />
        </main>
    );
}
