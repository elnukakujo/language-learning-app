import { BaseElement } from "@/interface/base";
import NavButton from "@/components/buttons/navButton";

export default function ElementSourcesCard({element} : {element: BaseElement}) {
    return (
        <section className="p-4 border rounded-md shadow-sm">
            <h2 className="text-lg font-semibold mb-2">Sources</h2>
            {element.sources && element.sources.length > 0 ? (
                <div className="flex flex-wrap gap-2">
                    {element.sources.map((source) => (
                        <NavButton
                            key={source.id}
                            className="inline-flex items-center gap-2 rounded-full bg-green-100 px-3 py-1 text-sm text-green-800"
                            path={`/sources/${source.id}`}
                        >
                            {source.title}
                        </NavButton>
                    ))}
                </div>
            ) : (
                <p className="text-gray-500">No sources assigned.</p>
            )}
        </section>
    );
}