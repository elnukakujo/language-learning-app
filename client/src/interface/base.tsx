import Source from "./systemData/Source";
import Tag from "./systemData/Tag";

export interface BaseElement {
    id: string;
    status: string;
    created_at: string;
    last_seen_at: string;
    score: number;

    tags?: Partial<Tag>[]; 
    sources?: Partial<Source>[];
}

export interface BaseMediaFiles {
    image_files?: string[];
    audio_files?: string[];
}

export interface BaseContainer extends BaseElement {
    level: number;
    description?: string;
}

export interface BaseFeature extends BaseElement, BaseMediaFiles {
    lesson_id: string;
    difficulty: number; // 0-1 scale, higher the harder
}

export interface BaseComponent extends BaseElement, BaseMediaFiles {
    language_id: string;
    difficulty: number; // 0-1 scale, higher the harder
}

export interface BaseDataCollection {
    id: string;
    user_id: string;
    language_id: string;
    created_at: string;
    updated_at?: string;
}