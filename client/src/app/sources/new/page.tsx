import SourceForm from "@/components/sources/sourceForm";

export default function NewSourcesPage() {
    return (
        <main className="flex flex-col gap-4">
            <h1>Create New Source</h1>
            <SourceForm />
        </main>
    );
}