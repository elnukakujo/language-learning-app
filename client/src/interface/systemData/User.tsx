import UserPreferences from "./UserPreferences";

export default interface User {
    id: string;
    username: string;
    last_review: string; // ISO date string
    created_at: string; // ISO date string
    preferences?: Partial<UserPreferences>; // Optional user preferences
}
