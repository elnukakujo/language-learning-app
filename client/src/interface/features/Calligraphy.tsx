import { BaseFeature } from "../base";

import Character from "../components/Character";
import Word from "../components/Word";

export default interface Calligraphy extends BaseFeature {
    character: Character;
    example_word?: Word;
};