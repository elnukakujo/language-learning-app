import { getAllUserSources } from "@/api";
import NavButton from "@/components/buttons/navButton";
import Source from "@/interface/systemData/Source";

export default async function SourcesPage() {
    const sources: Source[] = await getAllUserSources("user_U0");

    return (
        <div className="p-6">
            <div className="flex justify-between items-baseline mb-5">
                <h1 className="text-lg font-medium m-0">Sources</h1>
                <NavButton path="/sources/new">+ New</NavButton>
            </div>

            <ul className="list-none p-0 m-0 flex flex-col gap-0.5">
                {sources.map((source) => (
                <li key={source.id}>
                    <NavButton path={`/sources/${source.id}`} className="flex items-center gap-2.5 px-2 py-1.5 w-full">
                    <span className="w-2 h-2 rounded-full shrink-0" />
                    <span className="text-sm">{source.title}</span>
                    {source.description && (
                        <span className="text-xs opacity-40 ml-auto truncate">{source.description}</span>
                    )}
                    </NavButton>
                </li>
                ))}
            </ul>
        </div>
    );
}