"use client";

import { useState } from "react";
import SectionCard from "./sectionCard";
import AutoSizeTextArea from "@/components/ui/textArea/autoSizeTextArea";
import ClassicSelectMenu from "@/components/ui/selectMenu/classicSelectMenu";
import SaveButton from "./saveButton";
import ToggleRow from "./toggleRow";
import { updateUserPreferences } from "@/api/userPreferences";
import { LANGUAGE_to_ISO639_2T } from "@/utils/language_iso639";
import UserPreferences from "@/interface/systemData/UserPreferences";

const EXERCISE_TYPES = [
  "essay", "answering", "translate", "organize", "conversation",
  "type_in_the_blank", "select_in_the_blank", "matching", "true_false", "speaking",
];

const DIFFICULTY_LEVELS = [
  { value: "beginner", label: "Beginner" },
  { value: "intermediate", label: "Intermediate" },
  { value: "advanced", label: "Advanced" },
] as const;

const PRACTICE_MODES = [
  { value: "flashcards", label: "Flashcards" },
  { value: "listening", label: "Listening" },
  { value: "speaking", label: "Speaking" },
  { value: "writing", label: "Writing" },
] as const;

export default function PreferencesSection({ preferences }: { preferences: Partial<UserPreferences> }) {
  const [nativeLanguages, setNativeLanguages] = useState<string[]>(
    preferences.native_language_iso639_2 ?? []
  );
  const [learningGoals, setLearningGoals] = useState(preferences.learning_goals ?? "");
  const [exerciseTypes, setExerciseTypes] = useState<string[]>(
    preferences.preferred_exercise_types ?? []
  );
  const [dailyGoal, setDailyGoal] = useState(preferences.daily_goal_minutes ?? 20);
  const [difficulty, setDifficulty] = useState<string>("beginner"); // TODO: add to UserPreferences model
  const [practiceModes, setPracticeModes] = useState<string[]>(["flashcards"]); // TODO: add to UserPreferences model
  const [notifyEmail, setNotifyEmail] = useState(false); // TODO: add to UserPreferences model
  const [notifyInApp, setNotifyInApp] = useState(false); // TODO: add to UserPreferences model
  const [saving, setSaving] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);
    try {
      await updateUserPreferences(preferences.id!, {
        native_language_iso639_2: nativeLanguages,
        learning_goals: learningGoals,
        preferred_exercise_types: exerciseTypes,
        daily_goal_minutes: dailyGoal,
        // TODO: persist difficulty, practiceModes, notifications when backend supports them
      });
    } finally {
      setSaving(false);
    }
  };

  const toggleMode = (mode: string) => {
    setPracticeModes((prev) =>
      prev.includes(mode) ? prev.filter((m) => m !== mode) : [...prev, mode]
    );
  };

  return (
    <SectionCard title="Learning Preferences">
      <form onSubmit={handleSubmit} className="flex flex-col gap-4">
        {/* Target Language */}
        <ClassicSelectMenu
          label="Native Languages"
          options={Object.values(LANGUAGE_to_ISO639_2T)}
          selectedOption={nativeLanguages}
          onChange={(v) => setNativeLanguages(v as string[])}
          multiple
        />

        {/* Daily Goal */}
        <div className="flex flex-col gap-1">
          <span className="text-sm opacity-70">Daily Goal</span>
          <div className="flex items-center gap-3">
            <input
              type="range"
              className="flex-1 accent-[var(--color-primary)]"
              min={5}
              max={60}
              step={5}
              value={dailyGoal}
              onChange={(e) => setDailyGoal(Number(e.target.value))}
              disabled={saving}
              aria-label="Daily goal in minutes"
            />
            <input
              type="number"
              className="input w-16 text-center"
              min={5}
              max={60}
              step={5}
              value={dailyGoal}
              onChange={(e) => setDailyGoal(Number(e.target.value))}
              disabled={saving}
              aria-label="Daily goal minutes value"
            />
            <span className="text-sm opacity-60">min / day</span>
          </div>
        </div>

        {/* Difficulty */}
        <fieldset>
          <legend className="text-sm opacity-70 mb-1">Difficulty Level</legend>
          <div className="flex gap-3">
            {DIFFICULTY_LEVELS.map(({ value, label }) => (
              <label
                key={value}
                className={`flex items-center gap-1.5 text-sm cursor-pointer px-3 py-1.5 rounded-full border transition-colors ${
                  difficulty === value
                    ? "border-[var(--color-primary)] bg-[var(--color-primary)] text-[var(--color-primary-foreground)]"
                    : "border-[var(--color-border)] hover:border-[var(--color-muted)]"
                }`}
              >
                <input
                  type="radio"
                  name="difficulty"
                  value={value}
                  checked={difficulty === value}
                  onChange={(e) => setDifficulty(e.target.value)}
                  disabled={saving}
                  className="sr-only"
                />
                {label}
              </label>
            ))}
          </div>
        </fieldset>

        {/* Practice Modes */}
        <fieldset>
          <legend className="text-sm opacity-70 mb-1">Preferred Practice Modes</legend>
          <div className="flex flex-wrap gap-2">
            {PRACTICE_MODES.map(({ value, label }) => (
              <label
                key={value}
                className={`flex items-center gap-1.5 text-sm cursor-pointer px-3 py-1.5 rounded-full border transition-colors ${
                  practiceModes.includes(value)
                    ? "border-[var(--color-primary)] bg-[var(--color-primary)] text-[var(--color-primary-foreground)]"
                    : "border-[var(--color-border)] hover:border-[var(--color-muted)]"
                }`}
              >
                <input
                  type="checkbox"
                  checked={practiceModes.includes(value)}
                  onChange={() => toggleMode(value)}
                  disabled={saving}
                  className="sr-only"
                />
                {label}
              </label>
            ))}
          </div>
        </fieldset>

        {/* Learning Goals */}
        <AutoSizeTextArea
          label="Learning Goals"
          value={learningGoals}
          onChange={(e) => setLearningGoals(e.target.value)}
          placeholder="What do you want to achieve? e.g. Read a novel, hold a conversation..."
        />

        {/* Preferred Exercise Types */}
        <ClassicSelectMenu
          label="Preferred Exercise Types"
          options={EXERCISE_TYPES}
          selectedOption={exerciseTypes}
          onChange={(v) => setExerciseTypes(v as string[])}
          multiple
        />

        <div className="index-divider" />

        {/* Notifications */}
        <h3 className="text-sm font-medium">Notifications</h3>
        <ToggleRow
          label="Email reminders"
          description="Daily practice reminders via email"
          checked={notifyEmail}
          onChange={setNotifyEmail}
          disabled={saving}
        />
        <ToggleRow
          label="In-app notifications"
          description="Practice reminders and streak alerts"
          checked={notifyInApp}
          onChange={setNotifyInApp}
          disabled={saving}
        />

        <div>
          <SaveButton isLoading={saving} />
        </div>
      </form>
    </SectionCard>
  );
}
