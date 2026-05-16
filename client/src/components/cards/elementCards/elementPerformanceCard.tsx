import { BaseElement } from "@/interface/base";

export default function ElementPerformanceCard( {element} : { element: BaseElement }) {
    return (
        <section className="flex flex-col space-y-2 p-4 border rounded-md">
            <h3>Performance Information</h3>
            {'level' in element && (element as any).level != null && <p>Level: {(element as any).level}</p>}
            {'score' in element && (element as any).score != null && <p>Score: {(element as any).score.toFixed(2)}/100</p>}
            {'difficulty' in element && (element as any).difficulty != null && <p>Difficulty: {(element as any).difficulty.toFixed(2)}</p>}
            {'status' in element && (element as any).status != null && <p>Status: {(element as any).status}</p>}
            {'created_at' in element && (element as any).created_at != null && <p>Created at: {new Date((element as any).created_at).toLocaleDateString()}</p>}
            {'last_seen_at' in element && (element as any).last_seen_at != null && <p>Last seen at: {new Date((element as any).last_seen_at).toLocaleDateString()}</p>}
        </section>
    );
}