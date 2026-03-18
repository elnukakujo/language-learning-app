import Unit from "@/interface/containers/Unit";
import { getUnitData } from "@/api";
import UnitForm from "@/components/forms/entityForms/unitForm";

export default async function UpdateUnitPage({ params }: { params: { language_id: string, unit_id: string } }) {
    const { language_id, unit_id } = await params;

    const unit: Unit = await getUnitData(unit_id);

    return (
        <main>
            <h1>Update Unit</h1>
            <UnitForm language_id={language_id} unit={unit} />
        </main>
    );
}