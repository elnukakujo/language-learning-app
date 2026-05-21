"use client";

import { useEffect, useRef, useState } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faTimes, faChevronDown } from "@fortawesome/free-solid-svg-icons";

export default function ClassicSelectMenu({
  label,
  options,
  selectedOption,
  onChange,
  required = false,
  multiple = false,
}: {
  label: string;
  options: string[];
  selectedOption: string | string[];
  onChange: (value: string | string[]) => void;
  required?: boolean;
  multiple?: boolean;
}) {
  const [isOpen, setIsOpen] = useState(false);
  const [searchInput, setSearchInput] = useState("");
  const containerRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const selectedArray: string[] = multiple
    ? Array.isArray(selectedOption)
      ? selectedOption
      : selectedOption ? [selectedOption] : []
    : [];

  const singleValue = !multiple
    ? Array.isArray(selectedOption) ? (selectedOption[0] ?? "") : selectedOption
    : "";

  const formatLabel = (value: string) =>
    value.replace(/[-_]/g, " ").replace(/^./, (m) => m.toUpperCase());

  const filteredOptions = options.filter((opt) => {
    const matchesSearch = !searchInput || formatLabel(opt).toLowerCase().includes(searchInput.toLowerCase());
    const notSelected = multiple ? !selectedArray.includes(opt) : true;
    return matchesSearch && notSelected;
  });

  useEffect(() => {
    function handleClickOutside(e: MouseEvent) {
      if (containerRef.current && !containerRef.current.contains(e.target as Node)) {
        setIsOpen(false);
        setSearchInput("");
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const handleSelect = (option: string) => {
    if (!multiple) {
      onChange(option);
      setSearchInput("");
      setIsOpen(false);
      return;
    }
    const already = selectedArray.includes(option);
    onChange(already ? selectedArray.filter((o) => o !== option) : [...selectedArray, option]);
    setSearchInput("");
    inputRef.current?.focus();
  };

  const handleRemove = (option: string, e: React.MouseEvent) => {
    e.stopPropagation();
    onChange(selectedArray.filter((o) => o !== option));
  };

  const id = label.toLowerCase().replace(/\s+/g, "-");

  return (
    <div ref={containerRef} className="flex flex-col gap-1.5 w-full max-w-64">
      {label && (
        <label htmlFor={id} className="text-xs font-medium uppercase tracking-wide text-gray-500">
          {label} {required && <span className="text-red-500">*</span>}
        </label>
      )}

      {/* Trigger box */}
      <div
        onClick={() => { setIsOpen(true); inputRef.current?.focus(); }}
        className={`
          relative flex min-h-10 flex-wrap items-center gap-1.5 rounded-lg border px-2 py-1.5
          bg-white border-gray-300 cursor-text transition-colors
          focus-within:border-blue-400 focus-within:ring-2 focus-within:ring-blue-100
          ${isOpen ? "border-blue-400 ring-2 ring-blue-100" : ""}
        `}
      >
        {/* Multiple: chips */}
        {multiple && selectedArray.map((opt) => (
          <span
            key={opt}
            className="inline-flex items-center gap-1.5 rounded-full pl-2 pr-1 py-0.5 text-xs font-medium bg-blue-50 text-blue-800"
          >
            {formatLabel(opt)}
            <button
              type="button"
              onClick={(e) => handleRemove(opt, e)}
              className="flex h-4 w-4 items-center justify-center rounded-full text-blue-500 hover:bg-blue-200 hover:text-blue-900 transition-colors"
              aria-label={`Remove ${opt}`}
            >
              <FontAwesomeIcon icon={faTimes} className="text-[10px]" />
            </button>
          </span>
        ))}

        {/* Search input */}
        <input
          ref={inputRef}
          id={id}
          type="text"
          value={searchInput}
          onChange={(e) => { setSearchInput(e.target.value); setIsOpen(true); }}
          onFocus={() => setIsOpen(true)}
          placeholder={
            multiple
              ? selectedArray.length === 0 ? "Search or select…" : ""
              : singleValue ? "" : "Search or select…"
          }
          className="min-w-[80px] flex-1 bg-transparent text-sm text-gray-700 placeholder:text-gray-400 outline-none"
        />

        {/* Single mode: show selected value as faded overlay when not searching */}
        {!multiple && singleValue && !searchInput && (
          <span className="pointer-events-none absolute left-2 text-sm text-gray-700">
            {formatLabel(singleValue)}
          </span>
        )}

        <FontAwesomeIcon
          icon={faChevronDown}
          className={`ml-auto flex-shrink-0 text-gray-400 text-xs transition-transform ${isOpen ? "rotate-180" : ""}`}
        />
      </div>

      {/* Dropdown */}
      {isOpen && (
        <div
          role="listbox"
          aria-multiselectable={multiple}
          className="z-50 mt-1 max-h-52 overflow-y-auto rounded-lg border border-gray-200 bg-white shadow-md"
        >
          {filteredOptions.length === 0 ? (
            <p className="px-3 py-2 text-sm text-gray-400">No matching options</p>
          ) : (
            filteredOptions.map((option) => {
              const isSelected = !multiple && singleValue === option;
              return (
                <button
                  key={option}
                  type="button"
                  role="option"
                  aria-selected={isSelected}
                  onMouseDown={(e) => e.preventDefault()}
                  onClick={() => handleSelect(option)}
                  className={`
                    flex w-full items-center justify-between gap-2 px-3 py-2 text-left text-sm transition-colors
                    ${isSelected ? "bg-blue-50 text-blue-800 font-medium" : "text-gray-700 hover:bg-blue-50"}
                  `}
                >
                  {formatLabel(option)}
                  {isSelected && (
                    <span className="h-2 w-2 rounded-full bg-blue-500 flex-shrink-0" />
                  )}
                </button>
              );
            })
          )}
        </div>
      )}
    </div>
  );
}