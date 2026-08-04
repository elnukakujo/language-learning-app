"use client";

import { useState } from "react";
import SectionCard from "./sectionCard";
import ToggleRow from "./toggleRow";
import SaveButton from "./saveButton";
import { updateUserPreferences } from "@/api/userPreferences";
import { AlertTriangle } from "lucide-react";
import UserPreferences from "@/interface/systemData/UserPreferences";

const FEATURES = [
  { key: "feedback", label: "AI Feedback", desc: "Exercise feedback and corrections" },
  { key: "learnable", label: "Learnable Sentences", desc: "Contextual sentences for grammar points" },
  { key: "example", label: "Example Sentences", desc: "Usage examples for vocabulary words" },
  { key: "word", label: "Example Words", desc: "Word suggestions for calligraphy characters" },
  { key: "tts", label: "Text-to-Speech", desc: "Audio for words, sentences, and characters" },
] as const;

const DEFAULTS: Record<string, boolean> = {
  feedback: true, learnable: true, example: true, word: true, tts: true,
};

export default function AiFeaturesSection({
  prefId,
  preferences,
  hasEndpoints,
}: {
  prefId: string;
  preferences: Partial<UserPreferences>;
  hasEndpoints: boolean;
}) {
  const [toggles, setToggles] = useState({
    feedback: preferences.ai_feedback_enabled ?? true,
    learnable: preferences.ai_learnable_sentence_enabled ?? true,
    example: preferences.ai_example_sentence_enabled ?? true,
    word: preferences.ai_example_word_enabled ?? true,
    tts: preferences.ai_tts_enabled ?? true,
  });
  const [saving, setSaving] = useState(false);

  const anyEnabled = Object.values(toggles).some(Boolean);

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);
    try {
      await updateUserPreferences(prefId, {
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

  const resetToDefaults = () => {
    setToggles({
      feedback: true,
      learnable: true,
      example: true,
      word: true,
      tts: true,
    });
  };

  return (
    <SectionCard title="AI Features">
      <p className="text-sm opacity-60">
        Every feature runs through an API you connect yourself — nothing is bundled with the app.
      </p>

      {anyEnabled && !hasEndpoints && (
        <div
          className="flex items-center gap-2 text-sm rounded-lg p-3"
          style={{ background: "var(--color-accent-soft)", color: "var(--color-accent)" }}
          role="alert"
        >
          <AlertTriangle size={16} aria-hidden="true" />
          <span>AI features are enabled but no API endpoint is configured. Add one in the <strong>Endpoints</strong> section below.</span>
        </div>
      )}

      <form onSubmit={handleSave} className="flex flex-col gap-1">
        {FEATURES.map(({ key, label, desc }) => (
          <ToggleRow
            key={key}
            label={label}
            description={desc}
            checked={toggles[key]}
            onChange={(v) => setToggles((t) => ({ ...t, [key]: v }))}
            disabled={saving}
          />
        ))}

        <div className="flex items-center justify-between pt-3">
          <button
            type="button"
            className="text-xs opacity-50 hover:opacity-80 transition-opacity"
            onClick={resetToDefaults}
            disabled={saving}
          >
            Reset to defaults
          </button>
          <SaveButton isLoading={saving} />
        </div>
      </form>
    </SectionCard>
  );
}
