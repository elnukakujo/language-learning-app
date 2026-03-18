import UnitForm from "@/components/forms/entityForms/unitForm";

export default async function NewUnitPage({ params }: {params: { language_id: string } }) {
    const { language_id } = await params;

    return (
        <main>
            <h1>Create New Unit for Language ID: {language_id}</h1>
            <UnitForm language_id={language_id} />
        </main>
    );
}