"use client";

import { useState } from "react";
import SectionCard from "./sectionCard";
import SaveButton from "./saveButton";
import PasswordStrengthBar from "./passwordStrengthBar";
import { updateUserPassword } from "@/api/user";
import { Eye, EyeOff } from "lucide-react";

export default function PasswordSection({ userId }: { userId: string }) {
  const [currentPassword, setCurrentPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [showCurrent, setShowCurrent] = useState(false);
  const [showNew, setShowNew] = useState(false);
  const [showConfirm, setShowConfirm] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");

    if (!currentPassword && !newPassword && !confirmPassword) return;
    if (!currentPassword) { setError("Current password is required to set a new password"); return; }
    if (newPassword !== confirmPassword) { setError("New passwords do not match"); return; }
    if (newPassword.length < 8) { setError("New password must be at least 8 characters"); return; }

    setSaving(true);
    try {
      // TODO: include currentPassword in API call when backend supports verification
      await updateUserPassword(userId, newPassword);
      setCurrentPassword("");
      setNewPassword("");
      setConfirmPassword("");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to update password");
    } finally {
      setSaving(false);
    }
  };

  const passwordInput = (
    value: string,
    onChange: (v: string) => void,
    show: boolean,
    setShow: (v: boolean) => void,
    placeholder: string,
    autocomplete: string,
  ) => (
    <div className="relative">
      <input
        className="input pr-10"
        type={show ? "text" : "password"}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder={placeholder}
        autoComplete={autocomplete}
        disabled={saving}
      />
      <button
        type="button"
        className="absolute right-2 top-1/2 -translate-y-1/2 p-1.5 rounded-md opacity-50 hover:opacity-80 focus:outline-2 focus:outline-offset-1 focus:outline-[var(--color-accent)]"
        onClick={() => setShow(!show)}
        tabIndex={-1}
        aria-label={show ? "Hide password" : "Show password"}
      >
        {show ? <EyeOff size={16} /> : <Eye size={16} />}
      </button>
    </div>
  );

  return (
    <SectionCard title="Password">
      <p className="text-sm opacity-60">Leave all fields blank to keep your current password.</p>

      {error && (
        <p className="text-sm" style={{ color: "var(--color-danger)" }} role="alert">
          {error}
        </p>
      )}

      <form onSubmit={handleSubmit} className="flex flex-col gap-3">
        <label className="flex flex-col gap-1">
          <span className="text-sm opacity-70">Current Password</span>
          {passwordInput(currentPassword, setCurrentPassword, showCurrent, setShowCurrent, "Enter current password", "current-password")}
        </label>

        <div className="index-divider" />

        <label className="flex flex-col gap-1">
          <span className="text-sm opacity-70">New Password</span>
          {passwordInput(newPassword, setNewPassword, showNew, setShowNew, "Enter new password", "new-password")}
          {newPassword && <PasswordStrengthBar password={newPassword} />}
        </label>

        <label className="flex flex-col gap-1">
          <span className="text-sm opacity-70">Confirm New Password</span>
          {passwordInput(confirmPassword, setConfirmPassword, showConfirm, setShowConfirm, "Re-enter new password", "new-password")}
        </label>

        <div>
          <SaveButton isLoading={saving} onSuccessLabel="Password updated" />
        </div>
      </form>
    </SectionCard>
  );
}
