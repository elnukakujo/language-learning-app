import { BaseComponent } from '../base';

export default interface Character extends BaseComponent {
    character: string;
    phonetic: string;
    meaning?: string;
    radical?: string;
    strokes?: number;
}