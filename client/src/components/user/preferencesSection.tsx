"use client";

import { useState } from "react";
import SectionCard from "./sectionCard";
import AutoSizeTextArea from "@/components/ui/textArea/autoSizeTextArea";
import ClassicSelectMenu from "@/components/ui/selectMenu/classicSelectMenu";
import SaveButton from "./saveButton";
import { updateUserPreferences } from "@/api/userPreferences";
import { LANGUAGE_to_ISO639_2T } from "@/utils/language_iso639";
import UserPreferences from "@/interface/systemData/UserPreferences";

const EXERCISE_TYPES = [
  "essay", "answering", "translate", "organize", "conversation",
  "type_in_the_blank", "select_in_the_blank", "matching", "true_false", "speaking",
];

export default function PreferencesSection({ preferences }: { preferences: Partial<UserPreferences> }) {
  const [nativeLanguages, setNativeLanguages] = useState<string[]>(
    preferences.native_language_iso639_2 ?? []
  );
  const [learningGoals, setLearningGoals] = useState(preferences.learning_goals ?? "");
  const [exerciseTypes, setExerciseTypes] = useState<string[]>(
    preferences.preferred_exercise_types ?? []
  );
  const [dailyGoal, setDailyGoal] = useState(preferences.daily_goal_minutes ?? 20);
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
      });
    } finally {
      setSaving(false);
    }
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

        <div>
          <SaveButton isLoading={saving} />
        </div>
      </form>
    </SectionCard>
  );
}
