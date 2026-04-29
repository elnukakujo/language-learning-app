export default interface Source {
    id: string;
    user_id: string;
    title: string;
    date?: string; // ISO date string
    description?: string;
    source_type?: string; // e.g., 'book', 'website', 'video'
}
