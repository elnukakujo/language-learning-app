import { BASE_URL } from "..";
import Calligraphy from "@/interface/features/Calligraphy";

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