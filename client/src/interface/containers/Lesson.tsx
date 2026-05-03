import {BaseContainer} from '../base';

export default interface Lesson extends BaseContainer {
    id: string;
    title: string;
    
    user_id?: string;
    language_id: string;
    vocabulary?: string[];
    grammar?: string[];
    character_ids?: string[];
    exercise_ids?: string[];
};