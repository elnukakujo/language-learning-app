import { BaseFeature } from "../base";
import Calligraphy from "./Calligraphy";
import Grammar from "./Grammar";
import Vocabulary from "./Vocabulary";

export type ExerciseContent =
    | { segments: string[]; blanks: { options?: string[]; answer: string }[] } // type_in_the_blank / select_in_the_blank
    | { pairs: [string, string][] } // matching
    | { items: string[]; answer_order: number[] } // organize
    | { statement: string; answer: boolean }; // true_false

export default interface Exercise extends BaseFeature {
    exercise_type?: 'essay' | 'answering' | 'translate' | 'organize' | 'conversation' |
                    'type_in_the_blank' | 'select_in_the_blank' | 'matching' | 'true_false' | 'speaking';
    question: string;
    answer: string;
    text_support?: string;
    content?: ExerciseContent;

    related_vocabularies?: Partial<Vocabulary>[];
    related_calligraphies?: Partial<Calligraphy>[];
    related_grammars?: Partial<Grammar>[];
};