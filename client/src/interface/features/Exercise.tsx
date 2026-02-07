import { BaseFeature } from "../base";

export default interface Exercise extends BaseFeature {
    exercise_type?: 'essay' | 'answering' | 'translate' | 'organize' | 
                    'fill_in_the_blank' | 'matching' | 'true_false';
    question: string;
    answer: string;
    text_support?: string;
    vocabulary_ids?: string[];
    calligraphy_ids?: string[];
    grammar_ids?: string[];
};