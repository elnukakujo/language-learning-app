"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { createUser, updateUser } from "@/api/user";
import AutoWidthInput from "@/components/input/autoWidthInput";
import UpdateButton from "@/components/buttons/updateButton";
import NewElementButton from "@/components/buttons/newElementButton";
import User from "@/interface/systemData/User";
import ClassicSelectMenu from "@/components/selectMenu/classicSelectMenu";
import { LANGUAGE_to_ISO639_2T } from "@/utils/language_iso639";
import AutoSizeTextArea from "@/components/textArea/autoSizeTextArea";

export default function UserForm({ user, navDisabled = false, onSuccess }: { user?: User | Partial<User>, navDisabled?: boolean, onSuccess?: () => void }) {
    const isUpdate = Boolean(user?.id);
    const router = useRouter();

    const userData: Partial<User> = user ?? {
        id: "", username: "", last_review: new Date().toISOString(), created_at: new Date().toISOString()
    };

    const [username, setUsername] = useState<string>(userData.username || "");
    const [native_language_iso639_2, setNativeLanguageIso639_2] = useState<string[]>(userData.preferences?.native_language_iso639_2 || []);
    const [learning_goals, setLearningGoals] = useState<string>(userData.preferences?.learning_goals || "");
    const [preferred_exercise_types, setPreferredExerciseTypes] = useState<string[]>(userData.preferences?.preferred_exercise_types || []);

    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        const element: Partial<User> = {
            id: userData.id,
            username: username,
            last_review: userData.last_review,
            created_at: userData.created_at,
            preferences: {
                user_id: userData.id!,
                native_language_iso639_2: native_language_iso639_2,
                learning_goals: learning_goals,
                preferred_exercise_types: preferred_exercise_types
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
            </article>

            {isUpdate ? <UpdateButton>Update user</UpdateButton> : <NewElementButton>Add User</NewElementButton>}
        </form>
    );
}