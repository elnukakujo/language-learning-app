export default function ClassicSelectMenu({
  options,
  selectedOption,
  onChange,
}: {
  options: string[];
  selectedOption: string;
  onChange: (value: string) => void;
}) {
  return (
    <select
      value={selectedOption}
      onChange={(e) => onChange(e.target.value)}
      className="mt-1 block w-fit mx-auto pl-3 pr-10 py-2 text-base sm:text-sm rounded-md"
      required
    >
      <option value=""></option>
      {options.map((option) => (
        <option key={option} value={option}>
          {option.replace(/[-_]/g, ' ').replace(/^./, (match) => match.toUpperCase())}
        </option>
      ))}
    </select>
  );
}