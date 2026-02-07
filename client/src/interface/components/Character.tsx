import { BaseComponent } from '../base';

export default interface CharacterComponent extends BaseComponent {
    character: string;
    phonetic: string;
    meaning?: string;
    radical?: string;
    strokes?: number;
}