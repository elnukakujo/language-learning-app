import { BaseDataCollection } from "@/interface/base";

export default interface DailyStats extends BaseDataCollection {
    items_reviewed: number;
    items_correct: number;
    time_studied_ms: number;
    streak_day: number;
    current_streak_length: number;
}
