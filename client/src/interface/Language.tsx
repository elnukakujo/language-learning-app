export default interface Language {
    id: string;
    name: string;
    native_name: string;
    flag: string;
    level: string;
    current_unit_id?: string;
    description?: string;
    score: number;
    last_seen: Date;
};