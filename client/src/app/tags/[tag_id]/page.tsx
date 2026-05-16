import { getTagById } from "@/api";
import DeleteButton from "@/components/buttons/deleteButton";
import NavButton from "@/components/buttons/navButton";
import TagCard from "@/components/cards/tagCard";

export default async function TagDetailPage({ params }: { params: { tag_id: string } }) {
    const { tag_id } = await params;
    const tag = await getTagById(tag_id);
    console.log("Tag details:", tag);
    return (
        <main>
            <h1>Tag Detail</h1>
            <TagCard tag={tag} />
            <span className="flex flex-row gap-4">
                <NavButton path={`/tags/${tag_id}/update`}>
                    Edit Tag Informations
                </NavButton>
                <DeleteButton element_id={tag_id} />
            </span>
        </main>
    );
}