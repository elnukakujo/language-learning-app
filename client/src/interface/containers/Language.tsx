import { BaseContainer } from '../base';

export default interface Language extends BaseContainer {
    name: string;
    native_name?: string;
    flag?: string;
    level: 'A1' | 'A2' | 'B1' | 'B2' | 'C1' | 'C2';
    current_unit?: string;
    description?: string;
};