"use client";

import { useEffect, useRef, useState } from "react";
import Link from "next/link";
import { getAllUsers } from "@/api/user";
import { setUserCookie } from "@/utils/user_cookie";
import type User from "@/interface/systemData/User";

export default function UserSwitcher({ currentUserId }: { currentUserId: string | null }) {
    const [isOpen, setIsOpen] = useState(false);
    const [users, setUsers] = useState<User[]>([]);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState("");
    const containerRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        function handleClickOutside(event: MouseEvent) {
            if (containerRef.current && !containerRef.current.contains(event.target as Node)) {
                setIsOpen(false);
            }
        }
        document.addEventListener("mousedown", handleClickOutside);
        return () => document.removeEventListener("mousedown", handleClickOutside);
    }, []);

    const handleOpen = async () => {
        setIsOpen(true);
        setIsLoading(true);
        setError("");
        try {
            const response = await getAllUsers();
            setUsers(Array.isArray(response) ? response : []);
        } catch (err) {
            console.error("Failed to fetch users:", err);
            setError("Failed to load users");
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div ref={containerRef} className="relative">
            <button
                type="button"
                className="btn btn-secondary"
                onClick={() => (isOpen ? setIsOpen(false) : handleOpen())}
            >
                Switch User
            </button>

            {isOpen && (
                <div className="card absolute right-0 top-full z-50 mt-2 w-56 flex flex-col gap-1 p-2">
                    {isLoading ? (
                        <p className="px-2 py-1.5 text-sm text-muted">Loading…</p>
                    ) : error ? (
                        <p className="px-2 py-1.5 text-sm text-danger">{error}</p>
                    ) : users.length === 0 ? (
                        <p className="px-2 py-1.5 text-sm text-muted">No users found</p>
                    ) : (
                        users.map((user) => (
                            <button
                                key={user.id}
                                type="button"
                                disabled={user.id === currentUserId}
                                onClick={() => setUserCookie(user.id)}
                                className={`w-full rounded-md px-2 py-1.5 text-left text-sm transition-colors ${
                                    user.id === currentUserId
                                        ? "bg-accent-soft text-accent cursor-default"
                                        : "cursor-pointer text-foreground hover:bg-accent-soft"
                                }`}
                            >
                                {user.display_name || user.username}
                            </button>
                        ))
                    )}
                    <Link
                        href="/user/new"
                        className="mt-1 rounded-md border-t border-border px-2 py-1.5 pt-2 text-sm text-accent hover:bg-accent-soft"
                    >
                        + Add User
                    </Link>
                </div>
            )}
        </div>
    );
}
