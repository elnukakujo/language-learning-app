"use client";

import { useState } from "react";
import SectionCard from "./sectionCard";
import EditableField from "./editableField";
import { updateUser } from "@/api/user";
import User from "@/interface/systemData/User";

export default function ProfileSection({ user }: { user: User }) {
    const [username, setUsername] = useState(user.username ?? "");
    const [displayName, setDisplayName] = useState(user.display_name ?? "");
    const [email, setEmail] = useState(user.email ?? "");

    const handleSaveUsername = async (value: string) => {
        await updateUser(user.id, { username: value });
        setUsername(value);
    };

    const handleSaveDisplayName = async (value: string) => {
        await updateUser(user.id, { display_name: value || undefined });
        setDisplayName(value);
    };

    const handleSaveEmail = async (value: string) => {
        await updateUser(user.id, { email: value });
        setEmail(value);
    };

    return (
        <SectionCard title="Profile">
            <EditableField
                label="Username"
                value={username}
                onSave={handleSaveUsername}
                placeholder="your_username"
            />
            <EditableField
                label="Display Name"
                value={displayName}
                onSave={handleSaveDisplayName}
                placeholder="How your name appears"
            />
            <EditableField
                label="Email"
                value={email}
                onSave={handleSaveEmail}
                type="email"
                placeholder="you@example.com"
            />
        </SectionCard>
    );
}
