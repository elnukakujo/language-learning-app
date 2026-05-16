import { getSourceById } from "@/api";
import SourceForm from "@/components/forms/entityForms/sourceForm";

export default async function UpdateSourcePage({ params }: { params: { source_id: string } }) {
    const { source_id } = await params;
    const source = await getSourceById(source_id);
    return (
        <main>
            <h1>Update Source</h1>
            <SourceForm source={source} />
        </main>
    );
}