import { BaseContainer } from '../base';

export default interface Language extends BaseContainer {
    user_id?: string;
    name: string;
    native_name?: string;
    flag?: string;
    level: 'A1' | 'A2' | 'B1' | 'B2' | 'C1' | 'C2';
    current_lesson?: string;
    description?: string;
    lesson_ids?: string[];
};