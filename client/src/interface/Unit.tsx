export default interface Unit {
    id: string;
    title: string;
    description?: string;
    score?: number;
    last_seen?: Date;
};