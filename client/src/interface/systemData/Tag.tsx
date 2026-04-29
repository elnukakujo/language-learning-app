export default interface Tag {
    id: string;
    user_id: string;
    tagged_element_type: string; // e.g., 'vocabulary', 'grammar', 'exercise', ...
    name: string;
    color?: string;
    description?: string;
}
