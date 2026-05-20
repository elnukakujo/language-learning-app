import TagForm from "@/components/forms/entityForms/tagForm";
import { getTagById } from "@/api/tag";

export default async function UpdateTagPage({ params }: { params: { tag_id: string } }) {
    const { tag_id } = await params;
    const tag = await getTagById(tag_id);
    return (
        <main>
            <h1>Update Tag</h1>
            <TagForm tag={tag} />
        </main>
    );
}