"use client";

import User from '@/interface/systemData/User';
import { setUserCookie } from "@/utils/user_cookie";

export default function UserCard({ user, useCookie }: { user: User, useCookie?: boolean }) {
  return (
    <section
      className={`card flex flex-col space-y-4 ${useCookie ? "cursor-pointer hover:bg-accent-soft" : ""}`}
      onClick={() => useCookie && setUserCookie(user.id)}
    >
      <h3>{user.display_name || user.username}</h3>
      <div className="index-divider pt-3 flex flex-col gap-1">
        <p className="text-sm text-muted">Last review: {new Date(user.last_review).toLocaleDateString()}</p>
        <p className="text-sm text-muted">Created: {new Date(user.created_at).toLocaleDateString()}</p>
      </div>
    </section>
  );
}