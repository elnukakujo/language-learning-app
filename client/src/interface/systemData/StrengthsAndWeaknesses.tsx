export default interface StrengthsAndWeaknesses {
    id: string;
    user_id: string;
    language_id: string;
    language_name: string;
    element_type: string; // e.g., 'vocabulary', 'grammar', 'pronunciation'
    strengths: string;
    weaknesses: string;
    last_updated: string; // ISO date string
}
