"use client";

import CharacterBase from "@/interface/Character";
import ExerciseBase from "@/interface/Exercise";
import GrammarBase from "@/interface/Grammar";
import VocabularyBase from "@/interface/Vocabulary";

import { updateElement } from "@/api";
import { useRouter, useParams } from "next/navigation";

interface Character extends CharacterBase { type_element: 'char'; };
interface Grammar extends GrammarBase { type_element: 'gram'; };
interface Vocabulary extends VocabularyBase { type_element: 'voc'; };
interface Exercise extends ExerciseBase { type_element: 'ex'; };

type UpdateButtonProps = {
    element: Character | Grammar | Vocabulary | Exercise;
    children?: React.ReactNode;
};

export default function UpdateButton({ element, children }: UpdateButtonProps) {
    const elementId = element.id;
    const unitId = element.unit_id;
    const languageId = unitId.split('_')[0];
    const elementType = element.type_element;
    const router = useRouter();

    const handleUpdate = async () => {
        updateElement(element)
        .then(() => {
            console.log("Element updated successfully");
            router.push('/languages/' + languageId + '/unit/' + unitId + '/' + elementType + '/' + elementId);
        })
        .catch((error) => {
            console.error("Error updating element:", error);
        });
    };

    return (
        <button type="button" className="bg-blue-500 text-white rounded-md p-2" onClick={handleUpdate}>
            {children||"Update"}
        </button>
    );
}