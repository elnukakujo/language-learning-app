"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { createUser, updateUser } from "@/api/user";
import AutoWidthInput from "@/components/input/autoWidthInput";
import UpdateButton from "@/components/buttons/updateButton";
import NewElementButton from "@/components/buttons/newElementButton";
import User from "@/interface/systemData/User";

export default function UserForm({ user, navDisabled = false, onSuccess }: { user?: User | Partial<User>, navDisabled?: boolean, onSuccess?: () => void }) {
    const isUpdate = Boolean(user?.id);
    const router = useRouter();

    const userData: Partial<User> = user ?? {
        id: "", username: "", last_review: new Date().toISOString(), created_at: new Date().toISOString()
    };

    const [username, setUsername] = useState<string>(userData.username || "");

    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        const element: Partial<User> = {
            id: userData.id,
            username: username,
            last_review: userData.last_review,
            created_at: userData.created_at
        };
        try {
        if (isUpdate) {
            await updateUser(userData.id!, element);
        } else {
            await createUser(element);
        }
        if (!navDisabled) {
            router.push(`/`);
            router.refresh();
        }
        } catch (error) {
        console.error("Error creating/updating user:", error);
        alert(`Failed to ${isUpdate ? "update" : "create"} user.`);
        } finally {
        if (onSuccess) onSuccess();
        }
    };

    return (
        <form onSubmit={handleSubmit} className="flex flex-col gap-4 items-center">
            <AutoWidthInput
                label="Username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder="Enter username"
                required
            />

            {isUpdate ? <UpdateButton>Update user</UpdateButton> : <NewElementButton>Add User</NewElementButton>}
        </form>
    );
}