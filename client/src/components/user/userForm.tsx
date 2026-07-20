"use client";

import { useState } from "react";
import SubmitButton from "@/components/ui/buttons/submitButton";
import { useRouter } from "next/navigation";
import { createUser, updateUser } from "@/api/user";
import { updateUserPreferences } from "@/api/userPreferences";
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
    const [aiFeedbackEnabled, setAiFeedbackEnabled] = useState<boolean>(userData.preferences?.ai_feedback_enabled ?? true);
    const [aiLearnableSentenceEnabled, setAiLearnableSentenceEnabled] = useState<boolean>(userData.preferences?.ai_learnable_sentence_enabled ?? true);
    const [aiExampleSentenceEnabled, setAiExampleSentenceEnabled] = useState<boolean>(userData.preferences?.ai_example_sentence_enabled ?? true);
    const [aiExampleWordEnabled, setAiExampleWordEnabled] = useState<boolean>(userData.preferences?.ai_example_word_enabled ?? true);
    const [aiTtsEnabled, setAiTtsEnabled] = useState<boolean>(userData.preferences?.ai_tts_enabled ?? true);
    const [aiGenApiBaseUrl, setAiGenApiBaseUrl] = useState<string>(userData.preferences?.ai_gen_api_base_url || "");
    const [aiGenApiKey, setAiGenApiKey] = useState<string>(userData.preferences?.ai_gen_api_key || "");
    const [aiGenModel, setAiGenModel] = useState<string>(userData.preferences?.ai_gen_model || "");
    const [aiTtsApiBaseUrl, setAiTtsApiBaseUrl] = useState<string>(userData.preferences?.ai_tts_api_base_url || "");
    const [aiTtsApiKey, setAiTtsApiKey] = useState<string>(userData.preferences?.ai_tts_api_key || "");
    const [aiTtsModel, setAiTtsModel] = useState<string>(userData.preferences?.ai_tts_model || "");
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
                daily_goal_minutes: dailyGoalMinutes,
                ai_feedback_enabled: aiFeedbackEnabled,
                ai_learnable_sentence_enabled: aiLearnableSentenceEnabled,
                ai_example_sentence_enabled: aiExampleSentenceEnabled,
                ai_example_word_enabled: aiExampleWordEnabled,
                ai_tts_enabled: aiTtsEnabled
                // ai_gen_*/ai_tts_* connection fields are saved directly by ConnectionCapability
                // via PUT /api/pref/<id> as soon as you press Save there - not part of this submit.
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

            <article className="card w-full max-w-md flex flex-col gap-4">
                <div>
                    <h3>AI Features</h3>
                    <p className="text-xs" style={{ color: "var(--color-muted)" }}>
                        Every feature below runs through an API you connect yourself &mdash; nothing is bundled with the app.
                    </p>
                </div>

                <ConnectionCapability
                    title="Generation"
                    description="Writes example sentences, example words, and exercise feedback"
                    prefId={userData.preferences?.id}
                    baseUrl={aiGenApiBaseUrl}
                    apiKey={aiGenApiKey}
                    model={aiGenModel}
                    baseUrlField="ai_gen_api_base_url"
                    apiKeyField="ai_gen_api_key"
                    modelField="ai_gen_model"
                    onSaved={(v) => { setAiGenApiBaseUrl(v.baseUrl); setAiGenApiKey(v.apiKey); setAiGenModel(v.model); }}
                    baseUrlPlaceholder="e.g. http://localhost:8000/v1"
                    modelPlaceholder="e.g. Qwen/Qwen3-4B-AWQ"
                >
                    <AiToggleRow
                        label="Learnable sentences"
                        description="For grammar points"
                        checked={aiLearnableSentenceEnabled}
                        onChange={setAiLearnableSentenceEnabled}
                    />
                    <AiToggleRow
                        label="Example sentences"
                        description="For vocabulary words"
                        checked={aiExampleSentenceEnabled}
                        onChange={setAiExampleSentenceEnabled}
                    />
                    <AiToggleRow
                        label="Example words"
                        description="For calligraphy characters"
                        checked={aiExampleWordEnabled}
                        onChange={setAiExampleWordEnabled}
                    />
                    <AiToggleRow
                        label="Exercise feedback"
                        description="Otherwise falls back to a simple template"
                        checked={aiFeedbackEnabled}
                        onChange={setAiFeedbackEnabled}
                    />
                </ConnectionCapability>

                <div className="index-divider" />

                <ConnectionCapability
                    title="Speech"
                    description="Reads text aloud for characters, words, and passages"
                    prefId={userData.preferences?.id}
                    baseUrl={aiTtsApiBaseUrl}
                    apiKey={aiTtsApiKey}
                    model={aiTtsModel}
                    baseUrlField="ai_tts_api_base_url"
                    apiKeyField="ai_tts_api_key"
                    modelField="ai_tts_model"
                    onSaved={(v) => { setAiTtsApiBaseUrl(v.baseUrl); setAiTtsApiKey(v.apiKey); setAiTtsModel(v.model); }}
                    baseUrlPlaceholder="e.g. http://localhost:8091/v1"
                    modelPlaceholder="e.g. Qwen3-TTS-CustomVoice"
                >
                    <AiToggleRow
                        label="Audio generation"
                        description="Text-to-speech for new components"
                        checked={aiTtsEnabled}
                        onChange={setAiTtsEnabled}
                    />
                </ConnectionCapability>
            </article>

            {isUpdate ? <SubmitButton isLoading={isSubmitting}>Update user</SubmitButton> : <SubmitButton isLoading={isSubmitting}>Add User</SubmitButton>}
        </form>
    );
}

function AiToggleRow({
    label,
    description,
    checked,
    onChange,
}: {
    label: string;
    description: string;
    checked: boolean;
    onChange: (checked: boolean) => void;
}) {
    return (
        <label className="flex items-center justify-between gap-3 py-1.5">
            <span>
                <span className="block text-sm">{label}</span>
                <span className="block text-xs" style={{ color: "var(--color-muted)" }}>
                    {description}
                </span>
            </span>
            <input
                type="checkbox"
                className="h-5 w-5 shrink-0"
                style={{ accentColor: "var(--color-primary)" }}
                checked={checked}
                onChange={(e) => onChange(e.target.checked)}
            />
        </label>
    );
}

// A capability (e.g. "Generation", "Speech") backed by one API connection shared across its
// toggles. The connection is its own mini-form: read-only and dimmed until you press Edit, and
// Save writes straight to the database (PUT /api/pref/<id>) instead of waiting on the page's
// main submit - so the status badge always reflects what's actually stored, not a draft.
function ConnectionCapability({
    title,
    description,
    prefId,
    baseUrl,
    apiKey,
    model,
    baseUrlField,
    apiKeyField,
    modelField,
    onSaved,
    baseUrlPlaceholder,
    modelPlaceholder,
    children,
}: {
    title: string;
    description: string;
    prefId?: string;
    baseUrl: string;
    apiKey: string;
    model: string;
    baseUrlField: string;
    apiKeyField: string;
    modelField: string;
    onSaved: (values: { baseUrl: string; apiKey: string; model: string }) => void;
    baseUrlPlaceholder: string;
    modelPlaceholder: string;
    children: React.ReactNode;
}) {
    const [editing, setEditing] = useState(false);
    const [draftBaseUrl, setDraftBaseUrl] = useState(baseUrl);
    const [draftApiKey, setDraftApiKey] = useState(apiKey);
    const [draftModel, setDraftModel] = useState(model);
    const [saving, setSaving] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const isConnected = Boolean(baseUrl);

    const startEditing = () => {
        setDraftBaseUrl(baseUrl);
        setDraftApiKey(apiKey);
        setDraftModel(model);
        setError(null);
        setEditing(true);
    };

    const cancelEditing = () => {
        setError(null);
        setEditing(false);
    };

    const save = async () => {
        if (!prefId) {
            setError("Save this user first, then connect its API.");
            return;
        }
        const trimmedBaseUrl = draftBaseUrl.trim().replace(/\/+$/, "");
        if (trimmedBaseUrl) {
            let parsed: URL | null = null;
            try {
                parsed = new URL(trimmedBaseUrl);
            } catch {
                parsed = null;
            }
            if (!parsed || (parsed.protocol !== "http:" && parsed.protocol !== "https:")) {
                setError("Base URL must be a full address starting with http:// or https://");
                return;
            }
        }
        setSaving(true);
        setError(null);
        try {
            await updateUserPreferences(prefId, {
                [baseUrlField]: trimmedBaseUrl || undefined,
                [apiKeyField]: draftApiKey || undefined,
                [modelField]: draftModel || undefined,
            });
            onSaved({ baseUrl: trimmedBaseUrl, apiKey: draftApiKey, model: draftModel });
            setEditing(false);
        } catch {
            setError("Couldn't save this connection. Try again.");
        } finally {
            setSaving(false);
        }
    };

    return (
        <div className="flex flex-col gap-2">
            <div className="flex items-center justify-between gap-2">
                <div>
                    <span className="block text-sm font-medium">{title}</span>
                    <span className="block text-xs" style={{ color: "var(--color-muted)" }}>
                        {description}
                    </span>
                </div>
                <span
                    className="badge shrink-0"
                    style={!isConnected ? { background: "transparent", color: "var(--color-muted)", border: "1px solid var(--color-border)" } : { background: "var(--color-success)", color: "var(--color-primary-foreground)" }}
                >
                    <span
                        className="mr-1.5 inline-block h-1.5 w-1.5 rounded-full"
                        style={{ background: isConnected ? "var(--color-primary-foreground)" : "var(--color-muted)" }}
                    />
                    {isConnected ? "Connected" : "Not connected"}
                </span>
            </div>

            <div className="flex flex-col">
                {children}
            </div>

            <div
                className="flex flex-col gap-2 rounded-lg border p-3 transition-opacity"
                style={{
                    borderColor: "var(--color-border)",
                    background: editing ? "var(--color-surface)" : "transparent",
                    opacity: editing ? 1 : 0.55,
                }}
            >
                <div className="flex items-center justify-between gap-2">
                    <span className="text-xs font-medium" style={{ color: "var(--color-muted)" }}>
                        {isConnected ? (model || "Connection") : "No connection"}
                    </span>
                    {!editing && (
                        <button
                            type="button"
                            onClick={startEditing}
                            className="text-xs font-medium cursor-pointer"
                            style={{ color: "var(--color-accent)" }}
                        >
                            {isConnected ? "Edit" : "Connect"}
                        </button>
                    )}
                </div>

                <AutoWidthInput
                    label="Base URL"
                    value={editing ? draftBaseUrl : baseUrl}
                    onChange={(e) => setDraftBaseUrl(e.target.value)}
                    placeholder={baseUrlPlaceholder}
                    disabled={!editing}
                />
                <AutoWidthInput
                    type="password"
                    label="API Key"
                    value={editing ? draftApiKey : apiKey}
                    onChange={(e) => setDraftApiKey(e.target.value)}
                    placeholder="Leave blank if not required"
                    disabled={!editing}
                />
                <AutoWidthInput
                    label="Model"
                    value={editing ? draftModel : model}
                    onChange={(e) => setDraftModel(e.target.value)}
                    placeholder={modelPlaceholder}
                    disabled={!editing}
                />

                {error && <p className="text-xs" style={{ color: "var(--color-danger)" }}>{error}</p>}

                {editing && (
                    <div className="flex justify-end gap-2 pt-1">
                        <button
                            type="button"
                            onClick={cancelEditing}
                            disabled={saving}
                            className="text-xs font-medium cursor-pointer"
                            style={{ color: "var(--color-muted)" }}
                        >
                            Cancel
                        </button>
                        <button
                            type="button"
                            onClick={save}
                            disabled={saving}
                            className="text-xs font-medium cursor-pointer px-3 py-1 rounded-full"
                            style={{ background: "var(--color-primary)", color: "var(--color-primary-foreground)" }}
                        >
                            {saving ? "Saving…" : "Save"}
                        </button>
                    </div>
                )}
            </div>
        </div>
    );
}