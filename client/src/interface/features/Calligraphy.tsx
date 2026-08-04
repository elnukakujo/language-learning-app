import { BaseFeature } from "../base";

import Character from "../components/Character";
import Passage from "../components/Passage";
import Word from "../components/Word";

export default interface Calligraphy extends BaseFeature {
    character: Partial<Character>;

    example_words?: Partial<Word>[];
    example_sentences?: Partial<Passage>[];
};