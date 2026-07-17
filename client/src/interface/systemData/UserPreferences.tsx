import User from "./User";

export default interface UserPreferences {
    id: string;
    user_id: string;
    user?: User; 
    native_language_iso639_2: string[]; // Array of ISO 639-2 language codes
    learning_goals?: string;
    preferred_exercise_types?: string[]; // e.g., ['essay', 'translate']
    daily_goal_minutes?: number;
    last_updated: string; // ISO date string
    ai_feedback_enabled?: boolean;
    ai_text_gen_enabled?: boolean;
    ai_tts_enabled?: boolean;
}
