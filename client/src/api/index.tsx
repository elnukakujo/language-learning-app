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
  console.log(`Fetching element with ID: ${element_id}`);
  const res = await fetch(`${BASE_URL}/find_by_id/${element_id}`);
  if (!res.ok) throw new Error(`Failed to fetch vocabulary for element ${element_id}`);
  return res.json();
}