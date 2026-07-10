interface ScoreDisplayProps {
  score: number; // 0–100
}

const LEVELS = [
  { test: (s: number) => s === 0,  label: "Unstarted",   pip: "bg-muted",    text: "text-muted"   },
  { test: (s: number) => s < 75,   label: "In Progress", pip: "bg-warning",  text: "text-warning" },
  { test: (s: number) => s < 100,  label: "Revisiting",  pip: "bg-accent",   text: "text-accent"  },
  { test: (_: number) => true,     label: "Completed",   pip: "bg-success",  text: "text-success" },
] as const;

const PIPS = 5;

export default function ScoreDisplay({ score }: ScoreDisplayProps) {
  const clamped = Math.max(0, Math.min(100, score));
  const level = LEVELS.find((l) => l.test(clamped))!;
  const filledPips = clamped === 0 ? 0 : Math.max(1, Math.round((clamped / 100) * PIPS));

  return (
    <div className="inline-flex items-center gap-2">
      <span className="text-sm text-muted">Score</span>

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