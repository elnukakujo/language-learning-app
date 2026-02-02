import { getElementbyId, getLanguageData } from "@/api";
import type Grammar from "@/interface/features/Grammar";
import UpdateGrammarForm from "@/components/forms/updateForms/updateGrammarForm";

type paramsType = {
    language_id: string;
    unit_id: string;
    gram_id: string;
};

export default async function UpdateGrammarPage({ params }: { params: paramsType }) {
    const { gram_id, language_id } = await params;
    const grammar: Grammar = await getElementbyId(gram_id);
    const existingUnitsId: string[] = await getLanguageData(language_id).then(data => data.units.map((unit: {id: string}) => unit.id));


    return (
        <main className="flex flex-col items-center">
            <h1 className="text-2xl font-semibold mb-4">Update Grammar</h1>
            <UpdateGrammarForm grammar={grammar} existingUnitsId={existingUnitsId} />
        </main>
    );
}
