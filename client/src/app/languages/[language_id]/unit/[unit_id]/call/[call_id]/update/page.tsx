import { getElementbyId, getLanguageData } from "@/api";
import type Calligraphy from "@/interface/features/Calligraphy";
import UpdateCalligraphyForm from "@/components/forms/updateForms/updateCalligraphyForm";

type paramsType = {
    language_id: string;
    unit_id: string;
    call_id: string;
};

export default async function UpdateCalligraphyPage({ params }: { params: paramsType }) {
    const { call_id, language_id } = await params;
    const calligraphy: Calligraphy = await getElementbyId(call_id);

    return (
        <main className="p-4">
            <h1 className="text-2xl font-semibold mb-4">Update Calligraphy</h1>
            <UpdateCalligraphyForm calligraphy={calligraphy} />
        </main>
    );
}