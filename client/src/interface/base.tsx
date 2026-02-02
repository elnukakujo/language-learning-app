export interface BaseMediaFiles {
    image_files?: string[];
    audio_files?: string[];
}

export interface BaseComponent extends BaseMediaFiles {
    id?: string;
}

export interface BaseFeature extends BaseContainer, BaseMediaFiles {
    unit_id: string;
}

export interface BaseContainer {
    id?: string;
    score?: number;
    last_seen?: string; // ISO date string
}