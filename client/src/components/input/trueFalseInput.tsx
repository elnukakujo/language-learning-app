"use client";

export default function TrueFalseInput({
  value,
  onChange,
  label,
  className = "",
  placeholder = "",
  ...props
}: {
  value: boolean;
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  label?: string;
  className?: string;
  placeholder?: string;
}) {
  return (
    <div className={`flex flex-col space-y-2 ${className}`}>
      <label className="text-sm font-medium text-gray-700">
        {label}
      </label>
      <div className="flex items-center space-x-4">
        <label className="inline-flex items-center">
          <input
            type="radio"
            value="true"
            checked={value === true}
            onChange={(e) => onChange(e as React.ChangeEvent<HTMLInputElement>)}
            className="h-4 w-4 text-indigo-600 border-gray-300 rounded focus:ring-indigo-500"
            {...props}
          />
          <span className="ml-2">True</span>
        </label>
        <label className="inline-flex items-center">
          <input
            type="radio"
            value="false"
            checked={value === false}
            onChange={(e) => onChange(e as React.ChangeEvent<HTMLInputElement>)}
            className="h-4 w-4 text-indigo-600 border-gray-300 rounded focus:ring-indigo-500"
            {...props}
          />
          <span className="ml-2">False</span>
        </label>
      </div>
    </div>
  );
}