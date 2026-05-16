import type Language from "@/interface/containers/Language";
import type Lesson from "@/interface/containers/Lesson";
import type Calligraphy from "@/interface/features/Calligraphy";
import type Exercise from "@/interface/features/Exercise";
import type Grammar from "@/interface/features/Grammar";
import type Vocabulary from "@/interface/features/Vocabulary";
import Source from "@/interface/systemData/Source";
import Tag from "@/interface/systemData/Tag";

export const BASE_URL = process.env.LAPP_URL || "http://127.0.0.1:5000";

// ============= Language API =============
export async function getAvailableLanguages() {
  const res = await fetch(`${BASE_URL}/api/languages/`);
  if (!res.ok) throw new Error('Failed to fetch available languages');
  return res.json();
}

export async function getLanguageById(languageId: string) {
  const res = await fetch(`${BASE_URL}/api/languages/${languageId}`);
  if (!res.ok) throw new Error(`Failed to fetch language ${languageId}`);
  return res.json();
}

export async function getLanguageData(languageId: string) {
  const language: Language = await getLanguageById(languageId);
  const lessons = await fetch(`${BASE_URL}/api/lessons/all/${languageId}`);
  if (!lessons.ok) throw new Error(`Failed to fetch lessons for language ${languageId}`);
  const lessonsData: Lesson[] = await lessons.json();
  return {
    language,
    lessons: lessonsData,
  };
}

export async function createLanguage(data: Partial<Language>) {
  if (data.id) {
    data.id = undefined;
  }
  const res = await fetch(`${BASE_URL}/api/languages/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error("Failed to create language");
  return res.json();
}

export async function updateLanguage(languageId: string, data: Partial<Language>) {
  const res = await fetch(`${BASE_URL}/api/languages/${languageId}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error("Failed to update language");
  return res.json();
}

export async function deleteLanguage(languageId: string) {
  const res = await fetch(`${BASE_URL}/api/languages/${languageId}`, {
    method: "DELETE",
  });
  if (!res.ok) throw new Error("Failed to delete language");
}

// ============= Lesson API =============
export async function getLessonById(lesson_id: string) {
  const res = await fetch(`${BASE_URL}/api/lessons/${lesson_id}`);
  if (!res.ok) throw new Error(`Failed to fetch data for lesson ${lesson_id}`);
  return res.json();
}

export async function getAllLessons(languageId: string) {
  const res = await fetch(`${BASE_URL}/api/lessons/all/${languageId}`);
  if (!res.ok) throw new Error(`Failed to fetch lessons for language ${languageId}`);
  return res.json();
}

export async function createLesson(data: Partial<Lesson>) {
  if (data.id) {
    data.id = undefined;
  }
  const res = await fetch(`${BASE_URL}/api/lessons/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error("Failed to create lesson");
  return res.json();
}

export async function updateLesson(lessonId: string, data: Partial<Lesson>) {
  const res = await fetch(`${BASE_URL}/api/lessons/${lessonId}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error("Failed to update lesson");
  return res.json();
}

export async function deleteLesson(lessonId: string) {
  const res = await fetch(`${BASE_URL}/api/lessons/${lessonId}`, {
    method: "DELETE",
  });
  if (!res.ok) throw new Error("Failed to delete lesson");
}

// ============= Vocabulary API =============
export async function getVocabularyById(vocabularyId: string) {
  const res = await fetch(`${BASE_URL}/api/vocabulary/${vocabularyId}`);
  if (!res.ok) throw new Error(`Failed to fetch vocabulary ${vocabularyId}`);
  return res.json();
}

export async function getVocabularyByLanguage(languageId: string) {
  const res = await fetch(`${BASE_URL}/api/vocabulary/language/${languageId}`);
  if (!res.ok) throw new Error(`Failed to fetch vocabulary for language ${languageId}`);
  return res.json();
}

export async function getVocabularyByLesson(lessonId: string) {
  const res = await fetch(`${BASE_URL}/api/vocabulary/lesson/${lessonId}`);
  if (!res.ok) throw new Error(`Failed to fetch vocabulary for lesson ${lessonId}`);
  return res.json();
}

export async function createVocabulary(data: Partial<Vocabulary>) {
  if (data.id) {
    data.id = undefined;
  }
  const res = await fetch(`${BASE_URL}/api/vocabulary/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error("Failed to create vocabulary");
  return res.json();
}

export async function updateVocabulary(vocabularyId: string, data: Partial<Vocabulary>) {
  const res = await fetch(`${BASE_URL}/api/vocabulary/${vocabularyId}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error("Failed to update vocabulary");
  return res.json();
}

export async function deleteVocabulary(vocabularyId: string) {
  const res = await fetch(`${BASE_URL}/api/vocabulary/${vocabularyId}`, {
    method: "DELETE",
  });
  if (!res.ok) throw new Error("Failed to delete vocabulary");
}

// ============= Grammar API =============
export async function getGrammarById(grammarId: string) {
  const res = await fetch(`${BASE_URL}/api/grammar/${grammarId}`);
  if (!res.ok) throw new Error(`Failed to fetch grammar ${grammarId}`);
  return res.json();
}

export async function getGrammarByLanguage(languageId: string) {
  const res = await fetch(`${BASE_URL}/api/grammar/language/${languageId}`);
  if (!res.ok) throw new Error(`Failed to fetch grammar for language ${languageId}`);
  return res.json();
}

export async function getGrammarByLesson(lessonId: string) {
  const res = await fetch(`${BASE_URL}/api/grammar/lesson/${lessonId}`);
  if (!res.ok) throw new Error(`Failed to fetch grammar for lesson ${lessonId}`);
  return res.json();
}

export async function createGrammar(data: Partial<Grammar>) {
  if (data.id) {
    data.id = undefined;
  }
  const res = await fetch(`${BASE_URL}/api/grammar/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error("Failed to create grammar");
  return res.json();
}

export async function updateGrammar(grammarId: string, data: Partial<Grammar>) {
  const res = await fetch(`${BASE_URL}/api/grammar/${grammarId}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error("Failed to update grammar");
  return res.json();
}

export async function deleteGrammar(grammarId: string) {
  const res = await fetch(`${BASE_URL}/api/grammar/${grammarId}`, {
    method: "DELETE",
  });
  if (!res.ok) throw new Error("Failed to delete grammar");
}

// ============= Calligraphy API =============
export async function getCalligraphyById(calligraphyId: string) {
  const res = await fetch(`${BASE_URL}/api/calligraphy/${calligraphyId}`);
  if (!res.ok) throw new Error(`Failed to fetch calligraphy ${calligraphyId}`);
  return res.json();
}

export async function getCalligraphyByLanguage(languageId: string) {
  const res = await fetch(`${BASE_URL}/api/calligraphy/language/${languageId}`);
  if (!res.ok) throw new Error(`Failed to fetch calligraphy for language ${languageId}`);
  return res.json();
}

export async function getCalligraphyByLesson(lessonId: string) {
  const res = await fetch(`${BASE_URL}/api/calligraphy/lesson/${lessonId}`);
  if (!res.ok) throw new Error(`Failed to fetch calligraphy for lesson ${lessonId}`);
  return res.json();
}

export async function createCalligraphy(data: Partial<Calligraphy>) {
  if (data.id !== undefined) {
    delete data.id;
  }
  const res = await fetch(`${BASE_URL}/api/calligraphy/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error("Failed to create calligraphy");
  return res.json();
}

export async function updateCalligraphy(calligraphyId: string, data: Partial<Calligraphy>) {
  const res = await fetch(`${BASE_URL}/api/calligraphy/${calligraphyId}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error("Failed to update calligraphy");
  return res.json();
}

export async function deleteCalligraphy(calligraphyId: string) {
  const res = await fetch(`${BASE_URL}/api/calligraphy/${calligraphyId}`, {
    method: "DELETE",
  });
  if (!res.ok) throw new Error("Failed to delete calligraphy");
}

// ============= Exercise API =============
export async function getExerciseById(exerciseId: string) {
  const res = await fetch(`${BASE_URL}/api/exercise/${exerciseId}`);
  if (!res.ok) throw new Error(`Failed to fetch exercise ${exerciseId}`);
  return res.json();
}

export async function getExercisesByLanguage(languageId: string) {
  const res = await fetch(`${BASE_URL}/api/exercise/language/${languageId}`);
  if (!res.ok) throw new Error(`Failed to fetch exercises for language ${languageId}`);
  return res.json();
}

export async function getExercisesByLesson(lessonId: string) {
  const res = await fetch(`${BASE_URL}/api/exercise/lesson/${lessonId}`);
  if (!res.ok) throw new Error(`Failed to fetch exercises for lesson ${lessonId}`);
  return res.json();
}

export async function createExercise(data: Partial<Exercise>) {
  if (data.id !== undefined) {
    delete data.id;
  }
  const res = await fetch(`${BASE_URL}/api/exercise/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error("Failed to create exercise");
  return res.json();
}

export async function updateExercise(exerciseId: string, data: Partial<Exercise>) {
  const res = await fetch(`${BASE_URL}/api/exercise/${exerciseId}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error("Failed to update exercise");
  return res.json();
}

export async function deleteExercise(exerciseId: string) {
  const res = await fetch(`${BASE_URL}/api/exercise/${exerciseId}`, {
    method: "DELETE",
  });
  if (!res.ok) throw new Error("Failed to delete exercise");
}

// ============= Evaluation API =============
export async function evaluateText(exerciseId: string, userText: string) {
  const res = await fetch(`${BASE_URL}/api/evaluate/text`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ exercise_id: exerciseId, user_text: userText }),
  });
  if (!res.ok) throw new Error("Failed to evaluate text");
  return res.json();
}

export async function evaluateSpeech(exerciseId: string, user_audio_url: string, correct_audio_index: number = 0) {
  const res = await fetch(`${BASE_URL}/api/evaluate/speech`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ exercise_id: exerciseId, user_audio_url: user_audio_url, correct_audio_index: correct_audio_index }),
  });
  if (!res.ok) throw new Error("Failed to evaluate speech");
  return res.json();
}

// ============= Scoring API =============
export async function updateScoreById(elementId: string, score: number) {
  let endpoint = "";
  let payload: Record<string, string|number> = {};

  if (elementId.startsWith("voc_")) {
    endpoint = `${BASE_URL}/api/vocabulary/score/`;
    payload = { vocabulary_id: elementId, score: score };
  } else if (elementId.startsWith("gram_")) {
    endpoint = `${BASE_URL}/api/grammar/score`;
    payload = { grammar_id: elementId, score: score };
  } else if (elementId.startsWith("call_")) {
    endpoint = `${BASE_URL}/api/calligraphy/score`;
    payload = { calligraphy_id: elementId, score: score };
  } else if (elementId.startsWith("ex_")) {
    endpoint = `${BASE_URL}/api/exercise/score`;
    payload = { exercise_id: elementId, score: score };
  } else {
    throw new Error(`Unsupported element ID for scoring: ${elementId}`);
  }

  const res = await fetch(endpoint, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error("Failed to update score");
  return res.json();
}


// ============= Media API =============
export async function uploadImage(file: File, temporary = false) {
  const formData = new FormData();
  formData.append("file", file);
  if (temporary) {
    formData.append("temporary", "true");
  }

  try {
    const res = await fetch(`${BASE_URL}/media/upload/image`, {
      method: "POST",
      body: formData,
    });

    if (!res.ok) {
      const errorData = await res.json();
      throw new Error(errorData.detail || "Failed to upload image");
    }
    return await res.json();
  } catch (error) {
    console.error("Upload error:", error);
    throw error;
  }
}
export async function uploadAudio(file: File, temporary = false) {
  const formData = new FormData();
  formData.append("file", file);
  if (temporary) {
    formData.append("temporary", "true");
  }

  try {
    const res = await fetch(`${BASE_URL}/media/upload/audio`, {
      method: "POST",
      body: formData,
    });

    if (!res.ok) {
      const errorData = await res.json();
      throw new Error(errorData.detail || "Failed to upload audio");
    }
    return await res.json();
  } catch (error) {
    console.error("Upload error:", error);
    throw error;
  }
}

// ============= Tag API =============
export async function getAllUserTags(userId: string) {
  const res = await fetch(`${BASE_URL}/api/tags/user/${userId}`, {
    method: "GET",
    headers: { "Content-Type": "application/json" },
  });
  if (!res.ok) throw new Error("Failed to fetch user tags");
  return res.json();
}

export async function getTagById(tagId: string) {
  const res = await fetch(`${BASE_URL}/api/tags/${tagId}`, {
    method: "GET",
    headers: { "Content-Type": "application/json" },
  });
  if (!res.ok) throw new Error(`Failed to fetch tag ${tagId}`);
  return res.json();
}

export async function createTag(data: Partial<Tag>) {
  const res = await fetch(`${BASE_URL}/api/tags/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error("Failed to create tag");
  return res.json();
}

export async function updateTag(tagId: string, data: Partial<Tag>) {
  const res = await fetch(`${BASE_URL}/api/tags/${tagId}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error("Failed to update tag");
  return res.json();
}

export async function deleteTag(tagId: string) {
  const res = await fetch(`${BASE_URL}/api/tags/${tagId}`, {
    method: "DELETE",
  });
  if (!res.ok) throw new Error("Failed to delete tag");
}

export async function addTagToElement(tagId: string, elementId: string) {
  if (!tagId) throw new Error("addTagToElement: missing tagId");
  if (!elementId) throw new Error("addTagToElement: missing elementId - save the item before adding tags");

  const res = await fetch(`${BASE_URL}/api/tags/add_tag`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ tag_id: tagId, element_id: elementId }),
  });
  if (!res.ok) {
    const text = await res.text().catch(() => "");
    throw new Error(`Failed to add tag ${tagId} to element ${elementId}: ${res.status} ${text}`);
  }
  return res.json();
}

export async function removeTagFromElement(tagId: string, elementId: string) {
  if (!tagId) throw new Error("removeTagFromElement: missing tagId");
  if (!elementId) throw new Error("removeTagFromElement: missing elementId");

  const res = await fetch(`${BASE_URL}/api/tags/remove_tag`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ tag_id: tagId, element_id: elementId }),
  });
  if (!res.ok) {
    const text = await res.text().catch(() => "");
    throw new Error(`Failed to remove tag ${tagId} from element ${elementId}: ${res.status} ${text}`);
  }
  return res.json();
}

// ============= Source API =============
export async function getAllUserSources(userId: string) {
  const res = await fetch(`${BASE_URL}/api/sources/user/${userId}`, {
    method: "GET",
    headers: { "Content-Type": "application/json" },
  });
  if (!res.ok) throw new Error("Failed to fetch user sources");
  return res.json();
}

export async function getSourceById(sourceId: string) {
  const res = await fetch(`${BASE_URL}/api/sources/${sourceId}`, {
    method: "GET",
    headers: { "Content-Type": "application/json" },
  });
  if (!res.ok) throw new Error(`Failed to fetch source ${sourceId}`);
  return res.json();
}

export async function createSource(data: Partial<Source>) {
  const res = await fetch(`${BASE_URL}/api/sources/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error("Failed to create source");
  return res.json();
}

export async function updateSource(sourceId: string, data: Partial<Source>) {
  const res = await fetch(`${BASE_URL}/api/sources/${sourceId}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error("Failed to update source");
  return res.json();
}

export async function deleteSource(sourceId: string) {
  const res = await fetch(`${BASE_URL}/api/sources/${sourceId}`, {
    method: "DELETE",
  });
  if (!res.ok) throw new Error("Failed to delete source");
}

export async function addSourceToElement(sourceId: string, elementId: string) {
  const res = await fetch(`${BASE_URL}/api/sources/add_source`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ source_id: sourceId, element_id: elementId }),
  });
  if (!res.ok) throw new Error(`Failed to add source ${sourceId} to element ${elementId}`);
  return res.json();
}

export async function removeSourceFromElement(sourceId: string, elementId: string) {
  const res = await fetch(`${BASE_URL}/api/sources/remove_source`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ source_id: sourceId, element_id: elementId}),
  });
  if (!res.ok) throw new Error(`Failed to remove source ${sourceId} from element ${elementId}`);
  return res.json();
}

// ============= Legacy/Compatibility Functions =============
// These functions provide backward compatibility with existing code

export async function getElementbyId(element_id: string) {
  // Try to determine element type from ID prefix and fetch accordingly
  if (element_id.toLowerCase().startsWith('lang_')) {
    return getLanguageById(element_id);
  } else if (element_id.toLowerCase().startsWith('lesson_')) {
    return getLessonById(element_id);
  } else if (element_id.toLowerCase().startsWith('voc_')) {
    return getVocabularyById(element_id);
  } else if (element_id.toLowerCase().startsWith('gram_')) {
    return getGrammarById(element_id);
  } else if (element_id.toLowerCase().startsWith('call_')) {
    return getCalligraphyById(element_id);
  } else if (element_id.toLowerCase().startsWith('ex_')) {
    return getExerciseById(element_id);
  }
  throw new Error(`Unknown element type for ID: ${element_id}`);
}

const typeAliases: Record<string, string> = {
  lang: "Language",
  lesson: "Lesson",
  voc: "Vocabulary",
  gram: "Grammar",
  char: "Calligraphy",
  ex: "Exercise",
  language: "Language",
  vocabulary: "Vocabulary",
  grammar: "Grammar",
  calligraphy: "Calligraphy",
  exercise: "Exercise",
};

function normalizeType(type?: string) {
  if (!type) return type;
  return typeAliases[type] || type;
}

export async function updateElement(
  data: Calligraphy | Grammar | Vocabulary | Lesson | Language | Exercise
) {
  const { id, type_element } = data as any;
  const normalizedType = normalizeType(type_element);

  if (!id || !normalizedType) {
    throw new Error("Missing required fields: id or type_element");
  }

  // Route to appropriate update function based on type_element
  if (normalizedType === "Language" || id.startsWith("lang_")) {
    return updateLanguage(id, data as Partial<Language>);
  } else if (normalizedType === "Lesson" || id.startsWith("lesson_")) {
    return updateLesson(id, data as Partial<Lesson>);
  } else if (normalizedType === "Vocabulary" || id.startsWith("voc_")) {
    return updateVocabulary(id, data as Partial<Vocabulary>);
  } else if (normalizedType === "Grammar" || id.startsWith("gram_")) {
    return updateGrammar(id, data as Partial<Grammar>);
  } else if (normalizedType === "Calligraphy" || id.startsWith("call_")) {
    return updateCalligraphy(id, data as Partial<Calligraphy>);
  } else if (normalizedType === "Exercise" || id.startsWith("ex_")) {
    return updateExercise(id, data as Partial<Exercise>);
  }

  throw new Error(`Unknown element type: ${normalizedType}`);
}

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
  } else if (element_id.toLowerCase().startsWith('source_')) {
    return deleteSource(element_id);
  }
  throw new Error(`Unknown element type for ID: ${element_id}`);
}