export default interface Grammar {
    id: string;
    title: string;
    explanation: string;
    learnable_sentence?: string;
    score?: number;
    last_seen?: Date;
    unit_id: string;
};