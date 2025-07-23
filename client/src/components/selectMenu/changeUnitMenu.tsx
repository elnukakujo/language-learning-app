"use client";

export default function ChangeUnitMenu({ unitsId, unitId, onChange }: { unitsId: string[]; unitId: string; onChange: (id: string) => void }) {

    return (
        <select value={unitId} onChange={(e) => onChange(e.target.value)} className="flex w-full overflow-hidden border border-gray-300 rounded-md p-2">
            {unitsId.map((id) => (
                <option key={id} value={id}>
                    {id}
                </option>
            ))}
        </select>
    );
}