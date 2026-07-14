import type Calligraphy from "@/interface/features/Calligraphy";
import CalligraphyForm from "@/components/elements/calligraphyForm";
import { getCalligraphyById } from "@/api/calligraphy";

type paramsType = {
    language_id: string;
    lesson_id: string;
    call_id: string;
};

export default async function UpdateCalligraphyPage({ params }: { params: Promise<paramsType> }) {
    const { call_id, lesson_id } = await params;
    const calligraphy: Calligraphy = await getCalligraphyById(call_id);

    return (
        <main className="flex flex-col gap-4">
            <h1>Update Calligraphy</h1>
            <CalligraphyForm calligraphy={calligraphy} lesson_id={lesson_id} />
        </main>
    );
}