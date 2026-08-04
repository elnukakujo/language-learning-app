import { BASE_URL } from "..";
import UserPreferences from "@/interface/systemData/UserPreferences";

export async function updateUserPreferences(prefId: string, data: Partial<UserPreferences>) {
  const res = await fetch(`${BASE_URL}/api/pref/${prefId}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error("Failed to update user preferences");
  return res.json();
}
