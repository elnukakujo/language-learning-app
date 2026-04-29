import { BaseFeature } from "../base";
import Calligraphy from "./Calligraphy";
import Grammar from "./Grammar";
import Vocabulary from "./Vocabulary";

export default interface Exercise extends BaseFeature {
    exercise_type?: 'essay' | 'answering' | 'translate' | 'organize' | 'conversation' |
                    'type_in_the_blank' | 'select_in_the_blank' | 'matching' | 'true_false' | 'speaking';
    question: string;
    answer: string;
    text_support?: string;

    related_vocabularies?: Vocabulary[];
    related_calligraphies?: Calligraphy[];
    related_grammars?: Grammar[];
};