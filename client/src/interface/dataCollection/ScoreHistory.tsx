import { BaseDataCollection } from "@/interface/base";

export default interface ScoreHistory extends BaseDataCollection {
    element_id: string;
    element_type: string; // e.g., 'vocabulary', 'grammar', 'calligraphy', 'exercise'
    score_before: number;
    score_after: number;
}
