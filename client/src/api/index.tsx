import type Language from "@/interface/containers/Language";
import type Unit from "@/interface/containers/Unit";
import type Calligraphy from "@/interface/features/Calligraphy";
import type Exercise from "@/interface/features/Exercise";
import type Grammar from "@/interface/features/Grammar";
import type Vocabulary from "@/interface/features/Vocabulary";

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
  const language = await getLanguageById(languageId);
  const units = await fetch(`${BASE_URL}/api/units/all/${languageId}`);
  if (!units.ok) throw new Error(`Failed to fetch units for language ${languageId}`);
  const unitsData = await units.json();
  return {
    language,
    units: unitsData,
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

// ============= Unit API =============
export async function getUnitData(unit_id: string) {
  const res = await fetch(`${BASE_URL}/api/units/${unit_id}`);
  if (!res.ok) throw new Error(`Failed to fetch data for unit ${unit_id}`);
  return res.json();
}

export async function getAllUnits(languageId: string) {
  const res = await fetch(`${BASE_URL}/api/units/all/${languageId}`);
  if (!res.ok) throw new Error(`Failed to fetch units for language ${languageId}`);
  return res.json();
}

export async function createUnit(data: Partial<Unit>) {
  if (data.id) {
    data.id = undefined;
  }
  const res = await fetch(`${BASE_URL}/api/units/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error("Failed to create unit");
  return res.json();
}

export async function updateUnit(unitId: string, data: Partial<Unit>) {
  const res = await fetch(`${BASE_URL}/api/units/${unitId}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error("Failed to update unit");
  return res.json();
}

export async function deleteUnit(unitId: string) {
  const res = await fetch(`${BASE_URL}/api/units/${unitId}`, {
    method: "DELETE",
  });
  if (!res.ok) throw new Error("Failed to delete unit");
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

export async function getVocabularyByUnit(unitId: string) {
  const res = await fetch(`${BASE_URL}/api/vocabulary/unit/${unitId}`);
  if (!res.ok) throw new Error(`Failed to fetch vocabulary for unit ${unitId}`);
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

export async function getGrammarByUnit(unitId: string) {
  const res = await fetch(`${BASE_URL}/api/grammar/unit/${unitId}`);
  if (!res.ok) throw new Error(`Failed to fetch grammar for unit ${unitId}`);
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

export async function getCalligraphyByUnit(unitId: string) {
  const res = await fetch(`${BASE_URL}/api/calligraphy/unit/${unitId}`);
  if (!res.ok) throw new Error(`Failed to fetch calligraphy for unit ${unitId}`);
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

export async function getExercisesByUnit(unitId: string) {
  const res = await fetch(`${BASE_URL}/api/exercise/unit/${unitId}`);
  if (!res.ok) throw new Error(`Failed to fetch exercises for unit ${unitId}`);
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

export async function updateScoreById(elementId: string, success: boolean) {
  let endpoint = "";
  let payload: Record<string, string> = {};

  if (elementId.startsWith("voc_")) {
    endpoint = `${BASE_URL}/api/vocabulary/score/`;
    payload = { vocabulary_id: elementId, success: success.toString() };
  } else if (elementId.startsWith("gram_")) {
    endpoint = `${BASE_URL}/api/grammar/score`;
    payload = { grammar_id: elementId, success: success.toString() };
  } else if (elementId.startsWith("call_")) {
    endpoint = `${BASE_URL}/api/calligraphy/score`;
    payload = { calligraphy_id: elementId, success: success.toString() };
  } else if (elementId.startsWith("ex_")) {
    endpoint = `${BASE_URL}/api/exercise/score`;
    payload = { exercise_id: elementId, success: success.toString() };
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
export async function uploadImage(file: File) {
  const formData = new FormData();
  formData.append("file", file);

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

// ============= Legacy/Compatibility Functions =============
// These functions provide backward compatibility with existing code

export async function getElementbyId(element_id: string) {
  // Try to determine element type from ID prefix and fetch accordingly
  if (element_id.startsWith('lang_')) {
    return getLanguageById(element_id);
  } else if (element_id.startsWith('unit_')) {
    return getUnitData(element_id);
  } else if (element_id.startsWith('voc_')) {
    return getVocabularyById(element_id);
  } else if (element_id.startsWith('gram_')) {
    return getGrammarById(element_id);
  } else if (element_id.startsWith('call_')) {
    return getCalligraphyById(element_id);
  } else if (element_id.startsWith('ex_')) {
    return getExerciseById(element_id);
  }
  throw new Error(`Unknown element type for ID: ${element_id}`);
}

const typeAliases: Record<string, string> = {
  lang: "Language",
  unit: "Unit",
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
  data: Calligraphy | Grammar | Vocabulary | Unit | Language | Exercise
) {
  const { id, type_element } = data as any;
  const normalizedType = normalizeType(type_element);

  if (!id || !normalizedType) {
    throw new Error("Missing required fields: id or type_element");
  }

  // Route to appropriate update function based on type_element
  if (normalizedType === "Language" || id.startsWith("lang_")) {
    return updateLanguage(id, data as Partial<Language>);
  } else if (normalizedType === "Unit" || id.startsWith("unit_")) {
    return updateUnit(id, data as Partial<Unit>);
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
  if (element_id.startsWith('lang_')) {
    return deleteLanguage(element_id);
  } else if (element_id.startsWith('unit_')) {
    return deleteUnit(element_id);
  } else if (element_id.startsWith('voc_')) {
    return deleteVocabulary(element_id);
  } else if (element_id.startsWith('gram_')) {
    return deleteGrammar(element_id);
  } else if (element_id.startsWith('call_')) {
    return deleteCalligraphy(element_id);
  } else if (element_id.startsWith('ex_')) {
    return deleteExercise(element_id);
  }
  throw new Error(`Unknown element type for ID: ${element_id}`);
}

// Alias for backward compatibility
export async function getExercisesOverview(unit_id: string) {
  return getExercisesByUnit(unit_id);
}

// Note: getNext() function was removed as it doesn't exist in the new API
// If this functionality is needed, it should be implemented on the server side
export async function getNext(element_id: string) {
  throw new Error("getNext() is not implemented in the new API. Please implement this on the server side if needed.");
}