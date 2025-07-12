export default interface Vocabulary {
    id: string;
    word: string;
    translation: string;
    score?: number;
    last_seen?: Date;
    unit_id: string;
    type?: string;
    phonetic?: string;
    example_sentence?: string;
};