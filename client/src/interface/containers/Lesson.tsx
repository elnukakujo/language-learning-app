import {BaseContainer} from '../base';

export default interface Lesson extends BaseContainer {
    id: string;
    title: string;
    
    user_id?: string;
    language_id: string;
    vocabulary_ids?: string[];
    grammar_ids?: string[];
    character_ids?: string[];
    exercise_ids?: string[];
};