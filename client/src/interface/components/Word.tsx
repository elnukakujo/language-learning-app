import { BaseComponent } from '../base';

export default interface Word extends BaseComponent {
    word: string;
    translation: string;
    type: 'noun' | 'verb' | 'adjective' | 'adverb' | 'pronoun' | 'article' | 
    'preposition' | 'conjunction' | 'particle' | 'interjection' | 'numeral' | 
    'classifier' | 'auxiliary' | 'modal';
    phonetic?: string;
}
