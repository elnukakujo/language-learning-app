import { getSourceById } from "@/api/source";
import DeleteButton from "@/components/buttons/deleteButton";
import NavButton from "@/components/buttons/navButton";
import SourceCard from "@/components/cards/sourceCard";

export default async function SourceDetailPage({ params }: { params: { source_id: string } }) {
    const { source_id } = await params;
    const source = await getSourceById(source_id);
    return (
        <main>
            <h1>Source Detail</h1>
            <SourceCard source={source} />
            <span className="flex flex-row gap-4">
                <NavButton path={`/sources/${source_id}/update`}>
                    Edit Source Informations
                </NavButton>
                <DeleteButton element_id={source_id} />
            </span>
        </main>
    );
}