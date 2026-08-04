import { getSourceById } from "@/api/source";
import SourceForm from "@/components/sources/sourceForm";

export default async function UpdateSourcePage({ params }: { params: Promise<{ source_id: string }> }) {
    const { source_id } = await params;
    const source = await getSourceById(source_id);
    return (
        <main className="flex flex-col gap-4">
            <h1>Update Source</h1>
            <SourceForm source={source} />
        </main>
    );
}