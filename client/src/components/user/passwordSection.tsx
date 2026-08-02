"use client";

import { useState } from "react";
import SectionCard from "./sectionCard";
import AutoWidthInput from "@/components/ui/input/autoWidthInput";
import SubmitButton from "@/components/ui/buttons/submitButton";
import { updateUserPassword } from "@/api/user";

export default function PasswordSection({ userId }: { userId: string }) {
    const [newPassword, setNewPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");
    const [saving, setSaving] = useState(false);
    const [error, setError] = useState("");
    const [success, setSuccess] = useState(false);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError("");
        setSuccess(false);

        if (!newPassword && !confirmPassword) return; // blank = no-op
        if (newPassword !== confirmPassword) {
            setError("Passwords do not match");
            return;
        }

        setSaving(true);
        try {
            await updateUserPassword(userId, newPassword);
            setNewPassword("");
            setConfirmPassword("");
            setSuccess(true);
        } catch (err) {
            setError(err instanceof Error ? err.message : "Failed to update password");
        } finally {
            setSaving(false);
        }
    };

    return (
        <SectionCard title="Password">
            <p className="text-sm opacity-60">Optional — leave blank to keep your current password.</p>

            {error && <p className="text-sm text-red-500">{error}</p>}
            {success && <p className="text-sm" style={{ color: "var(--color-primary)" }}>Password updated.</p>}

            <form onSubmit={handleSubmit} className="flex flex-col gap-3">
                <AutoWidthInput
                    type="password"
                    value={newPassword}
                    onChange={(e) => setNewPassword(e.target.value)}
                    placeholder="New password"
                    disabled={saving}
                />
                <AutoWidthInput
                    type="password"
                    value={confirmPassword}
                    onChange={(e) => setConfirmPassword(e.target.value)}
                    placeholder="Confirm new password"
                    disabled={saving}
                />
                <div>
                    <SubmitButton isLoading={saving} />
                </div>
            </form>
        </SectionCard>
    );
}
