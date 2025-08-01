"use client";

import CharacterBase from "@/interface/Character";
import ExerciseBase from "@/interface/Exercise";
import GrammarBase from "@/interface/Grammar";
import VocabularyBase from "@/interface/Vocabulary";
import UnitBase from "@/interface/Unit";
import LanguageBase from "@/interface/Language";

import { updateElement } from "@/api";
import { useRouter } from "next/navigation";

interface Character extends CharacterBase { type_element: 'char'; };
interface Grammar extends GrammarBase { type_element: 'gram'; };
interface Vocabulary extends VocabularyBase { type_element: 'voc'; };
interface Exercise extends ExerciseBase { type_element: 'ex'; };
interface Unit extends UnitBase { type_element: 'unit'; };
interface Language extends LanguageBase { type_element: 'lang'; };


type UpdateButtonProps = {
    element: Character | Grammar | Vocabulary | Exercise | Unit | Language;
    children?: React.ReactNode;
};

export default function UpdateButton({ element, children }: UpdateButtonProps) {
    const router = useRouter();
    const elementType = element.type_element;

    const handleUpdate = async () => {
        const new_element = await updateElement(element);
        const elementId = new_element.id;
        const unitId = elementId.split('_').slice(0, 2).join('_');
        const languageId = elementId.split('_')[0];

        console.log(languageId, unitId, elementType, elementId);
        if (elementType === "lang") {
            router.push(`/languages/${languageId}`);
        } else if (elementType === 'unit') {
            router.push(`/languages/${languageId}/unit/${unitId}`);
        } else {
            router.push('/languages/' + languageId + '/unit/' + unitId + '/' + elementType + '/' + elementId);
        }
    };

    return (
        <button type="button" className="bg-blue-500 text-white rounded-md p-2" onClick={handleUpdate}>
            {children||"Update"}
        </button>
    );
}