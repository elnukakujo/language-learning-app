import { getElementbyId } from "@/api";
import type Grammar from "@/interface/Grammar";
import UpdateGrammarForm from "@/components/forms/updateForms/updateGrammarForm";

type paramsType = {
    language_id: string;
    unit_id: string;
    gram_id: string;
};

export default async function UpdateGrammarPage({ params }: { params: paramsType }) {
    const { gram_id } = await params;
    const grammar: Grammar = await getElementbyId(gram_id);

    return (
        <main className="p-4">
            <h1 className="text-2xl font-semibold mb-4">Update Grammar</h1>
            <UpdateGrammarForm grammar={grammar} />
        </main>
    );
}
