import {BaseFeature} from '../base';
import Passage from '../components/Passage';

export default interface Grammar extends BaseFeature {
    title: string;
    explanation: string;
    learnable_sentences?: Passage[];
};