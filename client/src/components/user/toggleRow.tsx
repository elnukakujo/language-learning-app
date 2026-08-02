"use client";

export default function ToggleRow({
  label,
  description,
  checked,
  onChange,
  disabled = false,
}: {
  label: string;
  description: string;
  checked: boolean;
  onChange: (checked: boolean) => void;
  disabled?: boolean;
}) {
  const id = `toggle-${label.toLowerCase().replace(/\s+/g, "-")}`;
  return (
    <label
      htmlFor={id}
      className={`flex items-center justify-between gap-3 py-2.5 ${
        disabled ? "opacity-50 cursor-not-allowed" : "cursor-pointer"
      }`}
    >
      <div className="flex flex-col">
        <span className="text-sm font-medium">{label}</span>
        <span className="text-xs opacity-50">{description}</span>
      </div>
      <input
        id={id}
        type="checkbox"
        className="toggle-switch"
        checked={checked}
        onChange={(e) => onChange(e.target.checked)}
        disabled={disabled}
        role="switch"
        aria-checked={checked}
      />
    </label>
  );
}
