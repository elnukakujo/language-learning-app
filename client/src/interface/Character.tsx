export default interface Character {
    id: string;
    character: string;
    translation: string;
    components: string;
    score: number;
    last_seen: Date;
    unit_id: string;
};