export default interface User {
    id: string;
    username: string;
    day_streaks: number;
    last_review: string; // ISO date string
    created_at: string; // ISO date string
}
