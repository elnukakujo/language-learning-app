interface BaseElement {
    id: string;
    status: string;
    created_at: string;
    last_seen_at: string;
    score: number;
}

interface BaseMediaFiles {
    image_files: string[];
    audio_files: string[];
}

export interface BaseContainer extends BaseElement {
    level: "A1" | "A2" | "B1" | "B2" | "C1" | "C2";
    description?: string;
}

export interface BaseFeature extends BaseElement, BaseMediaFiles {
    lesson_id: string;
    difficulty: number; // 0-1 scale, higher the harder
}

export interface BaseComponent extends BaseMediaFiles {
    language_id: string;
    difficulty: number; // 0-1 scale, higher the harder
}
