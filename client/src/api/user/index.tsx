import { BASE_URL } from "..";
import User from "@/interface/systemData/User";

export async function getAllUsers() {
  const res = await fetch(`${BASE_URL}/api/user/`, {
    method: "GET",
    headers: { "Content-Type": "application/json" },
  });
  if (!res.ok) throw new Error("Failed to fetch users");
  return res.json();
}

export async function getUserById(userId: string) {
  const res = await fetch(`${BASE_URL}/api/user/${userId}`, {
    method: "GET",
    headers: { "Content-Type": "application/json" },
  });
  if (!res.ok) throw new Error(`Failed to fetch user ${userId}`);
  return res.json();
}

export async function createUser(data: Partial<User>) {
  const res = await fetch(`${BASE_URL}/api/user/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error("Failed to create user");
  return res.json();
}

export async function updateUser(userId: string, data: Partial<User>) {
  const res = await fetch(`${BASE_URL}/api/user/${userId}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error("Failed to update user");
  return res.json();
}

export async function deleteUser(userId: string) {
  const res = await fetch(`${BASE_URL}/api/user/${userId}`, {
    method: "DELETE",
  });
  if (!res.ok) throw new Error("Failed to delete user");
}