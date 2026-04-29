export default interface UserPreferences {
    id: string;
    user_id: string;
    native_language_iso639_2: string[]; // Array of ISO 639-2 language codes
    learning_goals?: string;
    preferred_exercise_types?: string[]; // e.g., ['vocabulary', 'essay', 'translate']
    last_updated: string; // ISO date string
}
