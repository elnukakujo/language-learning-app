export default interface ProgressTracking {
    id: string;
    user_id: string;
    language_id: string;
    language_name: string;
    element_type: string; // e.g., 'vocabulary', 'grammar', 'calligraphy', 'exercise'
    element_status: string; // e.g., 'new', 'reviewing', 'mastered'
    new_score_difference: number;
    created_at: string; // ISO date string
    n_reviewed: number;
}
