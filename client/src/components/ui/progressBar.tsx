type ProgressBarProps = {
    current: number;
    total: number;
    showLabel?: boolean;
    showPercent?: boolean;
    className?: string;
};

export default function ProgressBar({
    current,
    total,
    showLabel = true,
    showPercent = true,
    className = "",
}: ProgressBarProps) {
    const percent = total > 0 ? Math.round((current / total) * 100) : 0;

    return (
        <div className={`flex flex-col gap-1.5 ${className}`}>
            {(showLabel || showPercent) && (
                <div className="flex justify-between text-sm" style={{ color: "var(--color-muted)" }}>
                    {showLabel && <span>{current} / {total}</span>}
                    {showPercent && <span>{percent}%</span>}
                </div>
            )}
            <div className="progress-bar-track">
                <div
                    className="progress-bar-fill"
                    style={{ width: `${percent}%` }}
                    role="progressbar"
                    aria-valuenow={current}
                    aria-valuemin={0}
                    aria-valuemax={total}
                />
            </div>
        </div>
    );
}