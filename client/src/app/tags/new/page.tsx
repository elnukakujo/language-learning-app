import TagForm from "@/components/tags/tagForm";

export default function NewTagsPage() {
    return (
        <main className="flex flex-col gap-4">
            <h1>Create New Tag</h1>
            <TagForm />
        </main>
    );
}