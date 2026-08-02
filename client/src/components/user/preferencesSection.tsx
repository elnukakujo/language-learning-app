"use client";

import { useState } from "react";
import SectionCard from "./sectionCard";
import AutoSizeTextArea from "@/components/ui/textArea/autoSizeTextArea";
import ClassicSelectMenu from "@/components/ui/selectMenu/classicSelectMenu";
import SubmitButton from "@/components/ui/buttons/submitButton";
import { updateUserPreferences } from "@/api/userPreferences";
import { LANGUAGE_to_ISO639_2T } from "@/utils/language_iso639";
import UserPreferences from "@/interface/systemData/UserPreferences";

const EXERCISE_TYPES = [
    "essay", "answering", "translate", "organize", "conversation",
    "type_in_the_blank", "select_in_the_blank", "matching", "true_false", "speaking",
];

const DAILY_GOAL_OPTIONS = ["5", "10", "15", "20", "30", "45", "60"];

export default function PreferencesSection({ preferences }: { preferences: Partial<UserPreferences> }) {
    const [nativeLanguages, setNativeLanguages] = useState<string[]>(
        preferences.native_language_iso639_2 ?? []
    );
    const [learningGoals, setLearningGoals] = useState(preferences.learning_goals ?? "");
    const [exerciseTypes, setExerciseTypes] = useState<string[]>(
        preferences.preferred_exercise_types ?? []
    );
    const [dailyGoal, setDailyGoal] = useState(
        (preferences.daily_goal_minutes ?? 20).toString()
    );
    const [toggles, setToggles] = useState({
        feedback: preferences.ai_feedback_enabled ?? true,
        learnable: preferences.ai_learnable_sentence_enabled ?? true,
        example: preferences.ai_example_sentence_enabled ?? true,
        word: preferences.ai_example_word_enabled ?? true,
        tts: preferences.ai_tts_enabled ?? true,
    });
    const [saving, setSaving] = useState(false);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setSaving(true);
        try {
            await updateUserPreferences(preferences.id!, {
                native_language_iso639_2: nativeLanguages,
                learning_goals: learningGoals,
                preferred_exercise_types: exerciseTypes,
                daily_goal_minutes: parseInt(dailyGoal),
                ai_feedback_enabled: toggles.feedback,
                ai_learnable_sentence_enabled: toggles.learnable,
                ai_example_sentence_enabled: toggles.example,
                ai_example_word_enabled: toggles.word,
                ai_tts_enabled: toggles.tts,
            });
        } finally {
            setSaving(false);
        }
    };

    return (
        <SectionCard title="Learning Preferences">
            <form onSubmit={handleSubmit} className="flex flex-col gap-3">
                <ClassicSelectMenu
                    label="Native Languages"
                    options={Object.values(LANGUAGE_to_ISO639_2T)}
                    selectedOption={nativeLanguages}
                    onChange={(v) => setNativeLanguages(v as string[])}
                    multiple
                />

                <AutoSizeTextArea
                    label="Learning Goals"
                    value={learningGoals}
                    onChange={(e) => setLearningGoals(e.target.value)}
                    placeholder="Enter learning goals"
                />

                <ClassicSelectMenu
                    label="Preferred Exercise Types"
                    options={EXERCISE_TYPES}
                    selectedOption={exerciseTypes}
                    onChange={(v) => setExerciseTypes(v as string[])}
                    multiple
                />

                <ClassicSelectMenu
                    label="Daily Goal (minutes)"
                    options={DAILY_GOAL_OPTIONS}
                    selectedOption={dailyGoal}
                    onChange={(v) => setDailyGoal(v as string)}
                />

                <div className="index-divider" />
                <h3>AI Features</h3>
                <p className="text-xs" style={{ color: "var(--color-muted)" }}>
                    Every feature below runs through an API you connect yourself — nothing is bundled with the app.
                </p>

                {([
                    ["feedback", "AI Feedback", "Exercise feedback and corrections"],
                    ["learnable", "Learnable Sentences", "For grammar points"],
                    ["example", "Example Sentences", "For vocabulary words"],
                    ["word", "Example Words", "For calligraphy characters"],
                    ["tts", "Text-to-Speech", "Audio for words, sentences, and characters"],
                ] as const).map(([key, label, desc]) => (
                    <label key={key} className="flex items-center gap-2 cursor-pointer">
                        <input
                            type="checkbox"
                            checked={toggles[key]}
                            onChange={(e) => setToggles((t) => ({ ...t, [key]: e.target.checked }))}
                        />
                        <span className="text-sm">
                            <span className="font-medium">{label}</span>
                            <span className="opacity-50"> — {desc}</span>
                        </span>
                    </label>
                ))}

                <div>
                    <SubmitButton isLoading={saving} />
                </div>
            </form>
        </SectionCard>
    );
}
