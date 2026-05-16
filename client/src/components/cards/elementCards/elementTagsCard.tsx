import { BaseElement } from "@/interface/base";
import NavButton from "@/components/buttons/navButton";

export default function ElementTagsCard({element} : {element: BaseElement}) {
    return (
        <section className="p-4 border rounded-md shadow-sm">
            <h2 className="text-lg font-semibold mb-2">Tags</h2>
            {element.tags && element.tags.length > 0 ? (
                <div className="flex flex-wrap gap-2">
                    {element.tags.map((tag) => (
                        <NavButton
                            key={tag.id}
                            className="inline-flex items-center gap-2 rounded-full bg-blue-100 px-3 py-1 text-sm text-blue-800"
                            path={`/tags/${tag.id}`}
                        >
                            {tag.color ? (
                                <span
                                    className="h-2 w-2 rounded-full"
                                    style={{ backgroundColor: tag.color }}
                                />
                            ) : null}
                            <span>{tag.name}</span>
                        </NavButton>
                    ))}
                </div>
            ) : (
                <p className="text-gray-500">No tags assigned.</p>
            )}
        </section>
    );
}