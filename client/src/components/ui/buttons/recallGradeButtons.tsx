export type RecallGrade = "again" | "hard" | "good" | "easy";

type GradeOption = {
    value: RecallGrade;
    label: string;
    hint: string;
    score: number;
};

const GRADES: GradeOption[] = [
    { value: "again", label: "Again", hint: "Blank",     score: 0 },
    { value: "hard",  label: "Hard",  hint: "Struggled", score: 0.5 },
    { value: "good",  label: "Good",  hint: "Recalled",  score: 0.75 },
    { value: "easy",  label: "Easy",  hint: "Instant",   score: 1 },
];

type RecallGradeButtonsProps = {
    onGrade: (score: number) => void;
};

export default function RecallGradeButtons({ onGrade }: RecallGradeButtonsProps) {
    return (
        <section className="flex flex-col gap-2">
            <p className="text-xs" style={{ color: "var(--color-muted)" }}>
                How well did you remember?
            </p>
            <div className="btn-row flex-wrap">
                {GRADES.map(({ value, label, hint, score }) => (
                    <button
                        key={value}
                        onClick={() => onGrade(score)}
                        className={`grade-btn grade-${value}`}
                    >
                        <span className="grade-dot" />
                        <span className="grade-label">{label}</span>
                        <span className="grade-hint">{hint}</span>
                    </button>
                ))}
            </div>
        </section>
    );
}