"use client";

function scorePassword(pw: string): { score: 0 | 1 | 2 | 3 | 4; label: string } {
  if (!pw) return { score: 0, label: "Too short" };
  let s = 0;
  if (pw.length >= 8) s++;
  if (pw.length >= 12) s++;
  if (/[A-Z]/.test(pw)) s++;
  if (/[0-9]/.test(pw)) s++;
  if (/[^A-Za-z0-9]/.test(pw)) s++;
  const clamped = Math.min(s, 4) as 0 | 1 | 2 | 3 | 4;
  const labels = ["Too short", "Weak", "Fair", "Good", "Strong"] as const;
  return { score: clamped, label: labels[clamped] };
}

const COLORS: Record<number, string> = {
  0: "var(--color-border)",
  1: "var(--color-danger)",
  2: "var(--color-warning)",
  3: "var(--color-primary)",
  4: "var(--color-success)",
};

export default function PasswordStrengthBar({ password }: { password: string }) {
  const { score, label } = scorePassword(password);
  return (
    <div className="flex flex-col gap-1" aria-live="polite">
      <div className="flex gap-1" role="progressbar" aria-valuenow={score} aria-valuemin={0} aria-valuemax={4} aria-label={`Password strength: ${label}`}>
        {[0, 1, 2, 3].map((i) => (
          <div
            key={i}
            className="strength-segment"
            style={{
              background: i < score ? COLORS[score] : "var(--color-border)",
              opacity: i < score ? 1 : 0.4,
            }}
          />
        ))}
      </div>
      <span className="text-xs opacity-60">{label}</span>
    </div>
  );
}
