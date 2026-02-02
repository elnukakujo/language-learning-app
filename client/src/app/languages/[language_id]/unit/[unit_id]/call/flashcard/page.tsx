import Calligraphy from "@/interface/features/Calligraphy";
import { getCalligraphyByUnit } from "@/api";
import CalligraphyFlashCard from "@/components/cards/characterFlashCard";

export default async function CalligraphyFlashCardPage({ params }: { params: { language_id: string; unit_id: string; }}) {
    const { unit_id } = await params;

    const calligraphies: Calligraphy[] = await getCalligraphyByUnit(unit_id);
    calligraphies.sort(() => Math.random() - 0.5); // Shuffle the array randomly

    return (
        <main>
            <h1>Calligraphy Flashcard</h1>
            <CalligraphyFlashCard calligraphies={calligraphies} />
        </main>
    );
}