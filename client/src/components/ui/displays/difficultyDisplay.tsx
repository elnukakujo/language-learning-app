interface DifficultyScoreProps {
  difficulty: number; // 0 (easy) → 1 (hard)
}

const LEVELS = [
  { max: 0.25, label: "Hard",    pip: "bg-danger",  text: "text-danger"  },
  { max: 0.5,  label: "Medium",  pip: "bg-accent",  text: "text-accent"  },
  { max: 0.75, label: "Easy",    pip: "bg-warning",   text: "text-warning"   },
  { max: 1.0,  label: "Trivial",  pip: "bg-success",   text: "text-success"   },
] as const;

const PIPS = 5;

export default function DifficultyDisplay({ difficulty }: DifficultyScoreProps) {
  const clamped = Math.max(0, Math.min(1, difficulty));
  const level = LEVELS.find((l) => clamped <= l.max) ?? LEVELS[LEVELS.length - 1];
  const filledPips = Math.round(clamped * PIPS);

  return (
    <div className="inline-flex items-center gap-2">
      <span className="text-sm text-muted">Difficulty</span>

      <div className="flex items-center gap-0.5">
        {Array.from({ length: PIPS }).map((_, i) => (
          <span
            key={i}
            className={`block w-1 h-3 rounded-full ${i < filledPips ? level.pip : "bg-border"}`}
          />
        ))}
      </div>

      <span className={`text-xs font-medium ${level.text}`}>
        {level.label}
      </span>
    </div>
  );
}