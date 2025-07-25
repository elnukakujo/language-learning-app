import Unit from "@/interface/Unit";
import { getUnitData } from "@/api";
import UpdateUnitForm from "@/components/forms/updateForms/updateUnitForm";

export default async function UpdateUnitPage({ params }: { params: { language_id: string, unit_id: string } }) {
    const { language_id, unit_id } = await params;

    const unit: Unit = await getUnitData(unit_id);

    return (
        <main>
            <h1>Update Unit</h1>
            <UpdateUnitForm unit={unit} />
        </main>
    );
}