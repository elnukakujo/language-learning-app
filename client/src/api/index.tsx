const BASE_URL = process.env.LAPP_URL || 'http://localhost:8000';

export async function getAvailableLanguages() {
  const res = await fetch(`${BASE_URL}/available_languages`);
  if (!res.ok) throw new Error('Failed to fetch available languages');
  return res.json();
}