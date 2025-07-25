import type Language from "@/interface/Language";
import type Unit from "@/interface/Unit";
import type Character from "@/interface/Character";
import type Exercise from "@/interface/Exercise";
import type Grammar from "@/interface/Grammar";
import type Vocabulary from "@/interface/Vocabulary";

const BASE_URL = process.env.LAPP_URL || 'http://localhost:8000';

export async function getAvailableLanguages() {
  const res = await fetch(`${BASE_URL}/available_languages`);
  if (!res.ok) throw new Error('Failed to fetch available languages');
  return res.json();
}

export async function getLanguageData(languageId: string) {
  const languages = await fetch(`${BASE_URL}/available_languages`);
  if (!languages.ok) throw new Error('Failed to fetch available languages');
  const languagesData = await languages.json();
  const language = languagesData.find((lang: { id: string }) => lang.id === languageId);

  const units = await fetch(`${BASE_URL}/units/${languageId}`);
  if (!units.ok) throw new Error(`Failed to fetch data for language ${languageId}`);
  const unitsData = await units.json();
  return {
    language,
    units: unitsData,
  };

  
}

export async function getUnitData(unit_id: string) {
  const res = await fetch(`${BASE_URL}/unit/${unit_id}`);
  if (!res.ok) throw new Error(`Failed to fetch data for unit ${unit_id}`);
  return res.json();
}

export async function getElementbyId(element_id: string) {
  const res = await fetch(`${BASE_URL}/find_by_id/${element_id}`);
  if (!res.ok) throw new Error(`Failed to fetch vocabulary for element ${element_id}`);
  return res.json();
}

export async function updateElement(
  data: Character | Grammar | Vocabulary | Unit | Language | Exercise
) {
  // Exclude last_seen and score using destructuring
  const { last_seen, score, type_element, ...updates } = data as any;

  const res = await fetch(`${BASE_URL}/update_by_id`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      element_id: data.id,
      updates,
    }),
  });

  if (!res.ok) throw new Error("Failed to update element");
  return res.json();
}

export async function addNewElement(
  data: Character | Grammar | Vocabulary | Unit | Language | Exercise
) {
  const { last_seen, score, type_element, id, ...newElement } = data as any;
  console.log(newElement);
  console.log(type_element.charAt(0).toLowerCase());
  const res = await fetch(`${BASE_URL}/new_element`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      element_type: type_element.charAt(0).toLowerCase(), // Get the first letter of the class name
      element: newElement,
    }),
  });

  if (!res.ok) throw new Error("Failed to add new element");
  return res.json();
}

export async function deleteElement(element_id: string) {
  const res = await fetch(`${BASE_URL}/delete_by_id/${element_id}`);

  if (!res.ok) throw new Error("Failed to delete element");
}

export async function getExercisesOverview(unit_id: string) {
  const res = await fetch(`${BASE_URL}/${unit_id}/exercises_overview`);

  if (!res.ok) throw new Error("Failed to get Exercises overview");
    return res.json();
}

export async function updateScoreById(ex_id: string, success: boolean) {
  const res = await fetch(`${BASE_URL}/update_score/`, {
    method: "POST",
    headers: { "Content-Type": "application/json"},
    body: JSON.stringify({ element_id: ex_id, success: success }),
  });

  if (!res.ok) throw new Error("Failed to update score by ID");
  return res.json();
}

export async function getNext(element_id: string) {
  const res = await fetch(`${BASE_URL}/next/${element_id}`);

  if (!res.ok) throw new Error("Failed to get next element");
  return res.json();
}