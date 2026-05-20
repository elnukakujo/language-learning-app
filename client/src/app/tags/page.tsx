import { getAllUserTags } from "@/api/tag";
import Tag from "@/interface/systemData/Tag";
import NavButton from "@/components/buttons/navButton";
import { getCurrentUserId } from "@/utils/user_cookie";

export default async function TagsPage() {
    const userId: string | null = await getCurrentUserId();
    const tags: Tag[] = await getAllUserTags(userId!);

    return (
        <div className="p-6">
            <div className="flex justify-between items-baseline mb-5">
                <h1 className="text-lg font-medium m-0">Tags</h1>
                <NavButton path="/tags/new">+ New</NavButton>
            </div>

            <ul className="list-none p-0 m-0 flex flex-col gap-0.5">
                {tags.map((tag) => (
                <li key={tag.id}>
                    <NavButton path={`/tags/${tag.id}`} className="flex items-center gap-2.5 px-2 py-1.5 w-full">
                    <span className="w-2 h-2 rounded-full shrink-0" style={{ backgroundColor: tag.color }} />
                    <span className="text-sm">{tag.name}</span>
                    {tag.description && (
                        <span className="text-xs opacity-40 ml-auto truncate">{tag.description}</span>
                    )}
                    </NavButton>
                </li>
                ))}
            </ul>
        </div>
    );
}