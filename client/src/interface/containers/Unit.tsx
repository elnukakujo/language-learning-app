import {BaseContainer} from '../base';

export default interface Unit extends BaseContainer {
    language_id: string;
    title: string;
    description?: string;
    level?: string;
    vocabulary_ids?: string[];
    grammar_ids?: string[];
    character_ids?: string[];
    exercise_ids?: string[];
};