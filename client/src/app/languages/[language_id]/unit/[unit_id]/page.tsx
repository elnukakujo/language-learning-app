import { getUnitData } from "@/api";

type Unit = {
    id: string;
    title: string;
    description: string;
    score: number;
};

export default async function Unit({ params }: { params: { language_id: string, unit_id: string } }) {
    const { unit_id } = await params;
    const unit: Unit = await getUnitData(unit_id);
    return (
        <main>
            <h1>{unit.title}</h1>
            <p>{unit.description}</p>
            <p>Score: {unit.score}</p>
        </main>
    );
}
