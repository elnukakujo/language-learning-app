export default interface Character {
    id: string;
    character: string;
    components?: string;
    phonetic?: string;
    meaning: string;
    example_word?: string;
    score?: number;
    last_seen?: Date;
    unit_id: string;
};