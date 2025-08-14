"use client";

import { useState, useRef, useEffect } from "react";

export default function AutoWidthInput({
  value,
  onChange,
  className = "",
  width = 20,
  ...props
}: React.InputHTMLAttributes<HTMLInputElement>) {
  const spanRef = useRef<HTMLSpanElement>(null);
  const [resizeWidth, setResizeWidth] = useState(width); // px

  useEffect(() => {
    if (spanRef.current) {
      setResizeWidth(spanRef.current.offsetWidth + Number(width)); // + small padding
    }
  }, [value]);

  return (
    <span className="inline-block relative">
      <span
        ref={spanRef}
        className="absolute invisible whitespace-pre text-base px-0"
      >
        {value || " "} {/* space so it’s never zero width */}
      </span>

      <input
        {...props}
        value={value ?? ""}
        onChange={onChange}
        style={{ width: resizeWidth }}
        className={`border-b text-center outline-none ${className}`}
      />
    </span>
  );
}