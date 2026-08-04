import { BaseComponent } from '../base';

export default interface Word extends BaseComponent {
    word: string;
    translation: string;
    word_type: 'noun' | 'verb' | 'adjective' | 'adverb' | 'pronoun' | 'article' | 
    'preposition' | 'conjunction' | 'particle' | 'interjection' | 'numeral' | 
    'classifier' | 'auxiliary' | 'modal';
    phonetic?: string;
    word_gender?: 'm' | 'f' | 'n' | 'c' | '';
}
