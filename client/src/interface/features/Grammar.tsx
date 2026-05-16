import {BaseFeature} from '../base';
import Word from '../components/Word';
import Passage from '../components/Passage';

export default interface Grammar extends BaseFeature {
    title: string;
    explanation: string;
    
    example_words?: Partial<Word>[];
    example_sentences?: Partial<Passage>[];
};