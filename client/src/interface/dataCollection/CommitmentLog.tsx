import { BaseDataCollection } from "@/interface/base";

export default interface CommitmentLog extends BaseDataCollection {
    week_start_date: string; // ISO date string representing the start of the week
    days_active: number; // number of days the user was active in that week
    total_items_reviewed: number; 
    total_time_ms: number; // total time studied in milliseconds for that week
    weekly_goal_met: boolean; // whether the user met their weekly goal
    longest_streak_ever: number; // longest streak ever achieved by the user up to that week
    streak_last_computed_at: string; // ISO date string when the longest streak was last updated
}
