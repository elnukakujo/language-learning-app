import Calligraphy from "@/interface/features/Calligraphy";
import Exercise from "@/interface/features/Exercise";
import Grammar from "@/interface/features/Grammar";
import Vocabulary from "@/interface/features/Vocabulary";
import Unit from "@/interface/containers/Unit";
import Language from "@/interface/containers/Language";

import { createCalligraphy, createExercise, createGrammar, createLanguage, createUnit, createVocabulary } from "@/api";
import { useRouter } from "next/navigation";

type NewElementButtonProps = {
    type: 'call' | 'gram' | 'voc' | 'ex' | 'unit' | 'lang';
    element: Calligraphy | Grammar | Vocabulary | Exercise | Unit | Language;
    children?: React.ReactNode;
};

export default function NewElementButton({ type, element, children }: NewElementButtonProps) {
    const router = useRouter();

    const handleCreate = async () => {
        if (type === 'lang') {
            createLanguage(element as Language).then(() => router.push(`/`));
        } else if (type === 'unit' && 'language_id' in element) {
            createUnit(element as Unit).then(() => router.push(`/languages/${element.language_id}`));
        } else if ((type === 'voc' || type === 'gram' || type === 'call' || type === 'ex') && 'unit_id' in element) {
            const router_path = '/languages/' + element.unit_id.split('_')[0].toUpperCase() + '/unit/' + element.unit_id;
            if (type === 'voc') {
                createVocabulary(element as Vocabulary).then(() => { router.push(router_path);})
            } else if (type === 'gram') {
                createGrammar(element as Grammar).then(() => { router.push(router_path);})
            } else if (type === 'call') {
                createCalligraphy(element as Calligraphy).then(() => { router.push(router_path);})
            } else if (type === 'ex') {
                createExercise(element as Exercise).then(() => { router.push(router_path);})
            }
        } else {
            throw new Error("Invalid element type or missing IDs for navigation.");
        }
    };

    return (
        <button type="button" className="bg-blue-500 text-white rounded-md p-2" onClick={handleCreate}>
            {children||"Add new element"}
        </button>
    );
}