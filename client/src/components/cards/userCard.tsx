"use client";

import User from '@/interface/systemData/User';
import { setUserCookie } from "@/utils/user_cookie";

export default function UserCard({ user, useCookie }: { user: User, useCookie?: boolean }) {
  return (
    <section
      className={`flex flex-col space-y-4 p-4 border rounded-md ${useCookie ? "cursor-pointer hover:bg-white/10" : ""}`}
      onClick={() => useCookie && setUserCookie(user.id)}
    >
      <h3>{user.username}</h3>
      <p>{new Date(user.last_review).toLocaleDateString()}</p>
      <p>{new Date(user.created_at).toLocaleDateString()}</p>
    </section>
  );
}