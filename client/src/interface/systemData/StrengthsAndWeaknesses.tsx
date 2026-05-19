export default interface StrengthsAndWeaknesses {
    id: string;
    user_id: string;
    language_id: string;
    element_type: string; // e.g., 'vocabulary', 'grammar', 'pronunciation'
    strengths: JSON;
    weaknesses: JSON;
    last_updated: string; // ISO date string
}
