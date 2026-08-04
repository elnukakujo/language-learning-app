import { BaseDataCollection } from "@/interface/base";

export default interface CommitmentLog extends BaseDataCollection {
    days_active: number; // number of days the user was active in that week
    total_items_reviewed: number; 
    total_time_ms: number; // total time studied in milliseconds for that week
    longest_streak_ever: number; // longest streak ever achieved by the user up to that week
    streak_last_computed_at: string; // ISO date string when the longest streak was last updated
}
