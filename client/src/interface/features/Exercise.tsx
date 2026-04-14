import { BaseFeature } from "../base";

export default interface Exercise extends BaseFeature {
    exercise_type?: 'essay' | 'answering' | 'translate' | 'organize' | 'conversation' |
                    'type_in_the_blank' | 'select_in_the_blank' | 'matching' | 'true_false' | 'speaking';
    question: string;
    answer: string;
    text_support?: string;
    vocabulary_ids?: string[];
    calligraphy_ids?: string[];
    grammar_ids?: string[];
};