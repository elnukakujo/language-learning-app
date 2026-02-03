import {BaseContainer} from '../base';

export default interface Unit extends BaseContainer {
    language_id: string;
    title: string;
    level: 'A1' | 'A2' | 'B1' | 'B2' | 'C1' | 'C2';
    description?: string;
    vocabulary_ids?: string[];
    grammar_ids?: string[];
    character_ids?: string[];
    exercise_ids?: string[];
};