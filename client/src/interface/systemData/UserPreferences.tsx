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
    ai_learnable_sentence_enabled?: boolean;
    ai_example_sentence_enabled?: boolean;
    ai_example_word_enabled?: boolean;
    ai_tts_enabled?: boolean;
    ai_gen_api_base_url?: string;
    ai_gen_api_key?: string;
    ai_gen_model?: string;
    ai_tts_api_base_url?: string;
    ai_tts_api_key?: string;
    ai_tts_model?: string;
}
