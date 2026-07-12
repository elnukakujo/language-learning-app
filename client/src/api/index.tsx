import { deleteLanguage } from "@/api/language";
import { deleteLesson } from "@/api/lesson";
import { deleteCalligraphy } from "@/api/calligraphy";
import { deleteExercise } from "@/api/exercise";
import { deleteGrammar } from "@/api/grammar";
import { deleteVocabulary } from "@/api/vocabulary";
import { deleteTag } from "@/api/tag";
import { deleteSource } from "@/api/source";

// NEXT_PUBLIC_ prefix required: this runs in the browser, not just the Next.js server.
export const BASE_URL = `http://${process.env.NEXT_PUBLIC_LAPP_HOST || "127.0.0.1"}:${process.env.NEXT_PUBLIC_LAPP_PORT || 5000}`;

// ============= Legacy/Compatibility Functions =============
// These functions provide backward compatibility with existing code

export async function deleteElement(element_id: string) {
  // Determine element type from ID prefix and delete accordingly
  if (element_id.toLowerCase().startsWith('lang_')) {
    return deleteLanguage(element_id);
  } else if (element_id.toLowerCase().startsWith('lesson_')) {
    return deleteLesson(element_id);
  } else if (element_id.toLowerCase().startsWith('voc_')) {
    return deleteVocabulary(element_id);
  } else if (element_id.toLowerCase().startsWith('gram_')) {
    return deleteGrammar(element_id);
  } else if (element_id.toLowerCase().startsWith('call_')) {
    return deleteCalligraphy(element_id);
  } else if (element_id.toLowerCase().startsWith('ex_')) {
    return deleteExercise(element_id);
  } else if (element_id.toLowerCase().startsWith('tag_')) {
    return deleteTag(element_id);
  } else if (element_id.toLowerCase().startsWith('src_')) {
    return deleteSource(element_id);
  }
  throw new Error(`Unknown element type for ID: ${element_id}`);
}