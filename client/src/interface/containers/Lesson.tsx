import {BaseContainer} from '../base';

export default interface Lesson extends BaseContainer {
    user_id?: string;
    language_id: string;
    lesson_id?: string;
    title: string;
    level: 'A1' | 'A2' | 'B1' | 'B2' | 'C1' | 'C2';
    description?: string;
    vocabulary_ids?: string[];
    grammar_ids?: string[];
    character_ids?: string[];
    exercise_ids?: string[];
};