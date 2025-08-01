import { getElementbyId, getLanguageData } from "@/api";
import type Character from "@/interface/Character";
import UpdateCharacterForm from "@/components/forms/updateForms/updateCharacterForm";

type paramsType = {
    language_id: string;
    unit_id: string;
    char_id: string;
};

export default async function UpdateCharacterPage({ params }: { params: paramsType }) {
    const { char_id, language_id } = await params;
    const character: Character = await getElementbyId(char_id);
    const existingUnitsId = await getLanguageData(language_id).then(data => data.units.map((unit: {id: string}) => unit.id));

    return (
        <main className="p-4">
            <h1 className="text-2xl font-semibold mb-4">Update Character</h1>
            <UpdateCharacterForm character={character} existingUnitsId={existingUnitsId} />
        </main>
    );
}