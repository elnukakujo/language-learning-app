"use client";

import { useState } from "react";
import SubmitButton from "@/components/ui/buttons/submitButton";
import { useRouter } from "next/navigation";
import { createUser, updateUser } from "@/api/user";
import AutoWidthInput from "@/components/ui/input/autoWidthInput";
import User from "@/interface/systemData/User";
import ClassicSelectMenu from "@/components/ui/selectMenu/classicSelectMenu";
import { LANGUAGE_to_ISO639_2T } from "@/utils/language_iso639";
import AutoSizeTextArea from "@/components/ui/textArea/autoSizeTextArea";

export default function UserForm({ user, navDisabled = false, onSuccess }: { user?: User | Partial<User>, navDisabled?: boolean, onSuccess?: () => void }) {
    const isUpdate = Boolean(user?.id);
    const router = useRouter();

    const userData: Partial<User> = user ?? {
        id: "", username: "", last_review: new Date().toISOString(), created_at: new Date().toISOString()
    };

    const [username, setUsername] = useState<string>(userData.username || "");
    const [displayName, setDisplayName] = useState<string>(userData.display_name || "");
    const [email, setEmail] = useState<string>(userData.email || "");
    const [password, setPassword] = useState<string>("");
    const [native_language_iso639_2, setNativeLanguageIso639_2] = useState<string[]>(userData.preferences?.native_language_iso639_2 || []);
    const [learning_goals, setLearningGoals] = useState<string>(userData.preferences?.learning_goals || "");
    const [preferred_exercise_types, setPreferredExerciseTypes] = useState<string[]>(userData.preferences?.preferred_exercise_types || []);
    const [dailyGoalMinutes, setDailyGoalMinutes] = useState<number>(userData.preferences?.daily_goal_minutes || 20);
    const [isSubmitting, setIsSubmitting] = useState(false);

    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        setIsSubmitting(true);
        const element: Partial<User> = {
            id: userData.id,
            username: username,
            display_name: displayName || undefined,
            email: email,
            ...(password ? { password } : {}),
            last_review: userData.last_review,
            created_at: userData.created_at,
            preferences: {
                user_id: userData.id!,
                native_language_iso639_2: native_language_iso639_2,
                learning_goals: learning_goals,
                preferred_exercise_types: preferred_exercise_types,
                daily_goal_minutes: dailyGoalMinutes
            }
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
        setIsSubmitting(false);
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

            <AutoWidthInput
                label="Display Name"
                value={displayName}
                onChange={(e) => setDisplayName(e.target.value)}
                placeholder="Shown instead of username, optional"
            />

            <AutoWidthInput
                type="email"
                label="Email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="Enter email"
                required={!isUpdate}
            />

            <AutoWidthInput
                type="password"
                label={isUpdate ? "New Password (leave blank to keep current)" : "Password"}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder={isUpdate ? "Leave blank to keep current password" : "Enter password"}
                required={!isUpdate}
            />

            <article className="flex flex-col space-y-2 items-center">
                <h3>User Preferences</h3>
                <ClassicSelectMenu
                    label="Native Languages"
                    options={Object.values(LANGUAGE_to_ISO639_2T)}
                    selectedOption={native_language_iso639_2}
                    onChange={(selected) => setNativeLanguageIso639_2(selected as string[])}
                    multiple
                />
                <AutoSizeTextArea
                    label="Learning Goals"
                    value={learning_goals}
                    onChange={(e) => setLearningGoals(e.target.value)}
                    placeholder="Enter learning goals"
                />
                <ClassicSelectMenu
                    label="Preferred Exercise Types"
                    options={['essay', 'answering', 'translate', 'organize', 'conversation', 'type_in_the_blank', 'select_in_the_blank', 'matching', 'true_false', 'speaking']}
                    selectedOption={preferred_exercise_types}
                    onChange={(selected) => setPreferredExerciseTypes(selected as string[])}
                    multiple
                />
                <ClassicSelectMenu
                    label="Daily Goal (minutes)"
                    options={['5', '10', '15', '20', '30', '45', '60']}
                    selectedOption={dailyGoalMinutes.toString()}
                    onChange={(selected) => setDailyGoalMinutes(parseInt((selected as string)))}
                />
            </article>

            {isUpdate ? <SubmitButton isLoading={isSubmitting}>Update user</SubmitButton> : <SubmitButton isLoading={isSubmitting}>Add User</SubmitButton>}
        </form>
    );
}