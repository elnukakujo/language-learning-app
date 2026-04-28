import Calligraphy from "@/interface/features/Calligraphy";
import { getCalligraphyByLesson } from "@/api";
import CalligraphyFlashCard from "@/components/cards/calligraphyFlashCard";

export default async function CalligraphyFlashCardPage({ params }: { params: { language_id: string; lesson_id: string; }}) {
    const { lesson_id } = await params;

    const calligraphies: Calligraphy[] = await getCalligraphyByLesson(lesson_id);
    calligraphies.sort(() => Math.random() - 0.5); // Shuffle the array randomly

    return (
        <main>
            <h1>Calligraphy Flashcard</h1>
            <CalligraphyFlashCard calligraphies={calligraphies} />
        </main>
    );
}