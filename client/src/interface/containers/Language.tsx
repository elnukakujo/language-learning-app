import { BaseContainer } from '../base';

export default interface Language extends BaseContainer {
    name: string;
    native_name?: string;
    flag?: string;
    target_iso639_2t?: string;
    source_iso639_2t?: string;
    
    user_id?: string;
    current_lesson_id?: string;
    lesson_ids?: string[];
};