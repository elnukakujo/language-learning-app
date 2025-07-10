import CharacterBase from "@/interface/Character";
import ExerciseBase from "@/interface/Exercise";
import GrammarBase from "@/interface/Grammar";
import VocabularyBase from "@/interface/Vocabulary";

import { addNewElement } from "@/api";
import { useRouter } from "next/navigation";

interface Character extends CharacterBase { type_element: 'char'; };
interface Grammar extends GrammarBase { type_element: 'gram'; };
interface Vocabulary extends VocabularyBase { type_element: 'voc'; };
interface Exercise extends ExerciseBase { type_element: 'ex'; };

type NewElementButtonProps = {
    element: Character | Grammar | Vocabulary | Exercise;
    children?: React.ReactNode;
};

export default function NewElementButton({ element, children }: NewElementButtonProps) {
    const router = useRouter();

    const handleCreate = async () => {
        addNewElement(element);
        router.push('/languages/' + element.unit_id.split('_')[0].toUpperCase() + '/unit/' + element.unit_id);
    };

    return (
        <button type="button" className="bg-blue-500 text-white rounded-md p-2" onClick={handleCreate}>
            {children||"Add new element"}
        </button>
    );
}