export default interface Tag {
    id: string;
    user_id: string;
    name: string;
    color?: string; // Hex color code, e.g., "#FF5733"
    description?: string;
    elements?: { string: string[] }; // Mapping of element types to arrays of element IDs
}
