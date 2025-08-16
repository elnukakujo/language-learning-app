"use client";

import { useState, useRef, useEffect } from "react";

export default function AutoWidthInput({
  value,
  onChange,
  label,
  className = "",
  minWidth = 12.5,
  maxWidth = 25,
  height = 2.5,
  placeholder = "",
  ...props

}: {
  value: string;
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  label?: string;
  className?: string;
  minWidth?: number;
  height?: number;
  maxWidth?: number;
  placeholder?: string;
}) {
  const spanRef = useRef<HTMLSpanElement>(null);
  const [resizeWidth, setResizeWidth] = useState<number>(minWidth);

  // Helper function to convert pixels to rem for state
  const pxToRem = (px: number) => px / parseFloat(getComputedStyle(document.documentElement).fontSize);

  useEffect(() => {
    if (spanRef.current) {
      const newWidth = pxToRem(spanRef.current.offsetWidth);
      console.log("New width:", newWidth);
      console.log("Min width:", minWidth, "Max width:", maxWidth);
      if (newWidth < minWidth) {
        setResizeWidth(minWidth);
      } else if (maxWidth) {
        setResizeWidth(newWidth > maxWidth ? maxWidth : newWidth);
      } else {
        setResizeWidth(newWidth);
      }
    }
  }, [value]);

  return (
    <span className="flex flex-col space-y-2">
      {label && 
        <label 
          htmlFor={label.toLowerCase().replace(/\s+/g, '-')} 
          className="text-sm font-medium text-gray-700"
        >
          {label}
        </label>
      }
      <span
      ref={spanRef}
      className="absolute invisible whitespace-pre text-base px-0"
      >
      {value || " "} {/* space so it’s never zero width */}
      </span>

      <input
        {...props}
        value={value ?? ""}
        onChange={(e) => onChange(e)}
        style={{ width: `${resizeWidth+1}rem`, height: `${height}rem` }}
        className={`outline-none rounded-md p-2 ${className}`}
        placeholder={placeholder}
      />
    </span>
  );
}