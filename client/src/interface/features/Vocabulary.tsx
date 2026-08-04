import { BaseFeature } from '../base';
import Word from '../components/Word';
import Passage from '../components/Passage';

export default interface Vocabulary extends BaseFeature {
    word: Partial<Word>;
    example_sentences?: Partial<Passage>[];
};