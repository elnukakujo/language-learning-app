export default interface Exercise {
    id: string;
    exercise_type?: string;
    question: string;
    support?: string;
    answer: string;
    score?: number;
    last_seen?: Date;
    unit_id: string;
    associated_to?: { [key: string]: string[] };
};