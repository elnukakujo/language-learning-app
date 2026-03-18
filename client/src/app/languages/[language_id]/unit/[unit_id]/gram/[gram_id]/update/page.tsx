import { getElementbyId } from "@/api";
import type Grammar from "@/interface/features/Grammar";
import GrammarForm from "@/components/forms/entityForms/grammarForm";

type paramsType = {
    language_id: string;
    unit_id: string;
    gram_id: string;
};

export default async function UpdateGrammarPage({ params }: { params: paramsType }) {
    const { gram_id } = await params;
    const grammar: Grammar = await getElementbyId(gram_id);

    return (
        <main className="flex flex-col items-center">
            <h1 className="text-2xl font-semibold mb-4">Update Grammar</h1>
            <GrammarForm grammar={grammar} unit_id={params.unit_id} />
        </main>
    );
}
