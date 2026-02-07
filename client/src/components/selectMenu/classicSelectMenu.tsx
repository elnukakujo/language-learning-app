export default function ClassicSelectMenu({
  label,
  options,
  selectedOption,
  onChange,
  required = false,
}: {
  label: string;
  options: string[];
  selectedOption: string;
  onChange: (value: string) => void;
  required?: boolean;
}) {
  return (
    <span className="mt-1 flex flex-col space-y-2 w-full max-w-64 mx-auto pl-3 pr-10 text-base sm:text-sm rounded-md">
      {label && 
          <label 
            htmlFor={label.toLowerCase().replace(/\s+/g, '-')} 
            className="text-sm font-medium text-gray-700"
          >
            {label} {required && "*"}
          </label>
        }
      <select
        value={selectedOption}
        onChange={(e) => onChange(e.target.value)}
        required={required}
      >
        <option value="" disabled={required}>
          Select an option
        </option>
        {options.map((option) => (
          <option key={option} value={option}>
            {option.replace(/[-_]/g, ' ').replace(/^./, (match) => match.toUpperCase())}
          </option>
        ))}
      </select>
    </span>
  );
}