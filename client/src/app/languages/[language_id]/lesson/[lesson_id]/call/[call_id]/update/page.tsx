import type Calligraphy from "@/interface/features/Calligraphy";
import CalligraphyForm from "@/components/forms/entityForms/calligraphyForm";
import { getCalligraphyById } from "@/api/calligraphy";

type paramsType = {
    language_id: string;
    lesson_id: string;
    call_id: string;
};

export default async function UpdateCalligraphyPage({ params }: { params: paramsType }) {
    const { call_id } = await params;
    const calligraphy: Calligraphy = await getCalligraphyById(call_id);

    return (
        <main className="p-4">
            <h1 className="text-2xl font-semibold mb-4">Update Calligraphy</h1>
            <CalligraphyForm calligraphy={calligraphy} lesson_id={params.lesson_id} />
        </main>
    );
}