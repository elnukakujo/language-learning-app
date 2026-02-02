import { BaseContainer } from '../base';

export default interface Language extends BaseContainer {
    name: string;
    native_name?: string;
    flag?: string;
    level?: string;
    current_unit?: string;
    description?: string;
};