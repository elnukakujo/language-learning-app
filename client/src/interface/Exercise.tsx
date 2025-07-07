export default interface Exercise {
    id: string;
    type: string;
    question: string;
    support: string;
    answer: string;
    score: number;
    last_seen: Date;
    unit_id: string;
};