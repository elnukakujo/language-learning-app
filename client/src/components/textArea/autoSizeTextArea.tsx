"use client";
import { useRef, useEffect, useState } from "react";

export default function AutoSizeTextArea({
  value,
  onChange,
  label,
  className = "",
  minWidth = 12.5,
  minHeight = 2.5,
  maxWidth = 25,
  maxHeight,
  placeholder = "",
  ...props
}: {
  value: string;
  onChange: (e: React.ChangeEvent<HTMLTextAreaElement>) => void;
  label?: string;
  className?: string;
  minWidth?: number;
  minHeight?: number;
  maxWidth?: number;
  maxHeight?: number;
  placeholder?: string;
}) {
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const [dimensions, setDimensions] = useState({ width: minWidth, height: minHeight });

  // Helper function to convert rem to pixels for calculations
  const remToPx = (rem: number) => rem * parseFloat(getComputedStyle(document.documentElement).fontSize);
  
  // Helper function to convert pixels to rem for state
  const pxToRem = (px: number) => px / parseFloat(getComputedStyle(document.documentElement).fontSize);

  const adjustSize = () => {
    const textarea = textareaRef.current;
    if (!textarea) return;

    // Store original styles
    const originalWidth = textarea.style.width;
    const originalHeight = textarea.style.height;
    const originalWhiteSpace = textarea.style.whiteSpace;
    const originalOverflow = textarea.style.overflow;

    // Convert rem to pixels for calculations
    const minWidthPx = remToPx(minWidth);
    const minHeightPx = remToPx(minHeight);
    const maxWidthPx = maxWidth ? remToPx(maxWidth) : undefined;
    const maxHeightPx = maxHeight ? remToPx(maxHeight) : undefined;

    // First, measure height with current width
    textarea.style.height = 'auto';
    textarea.style.overflow = 'hidden';
    let newHeightPx = Math.max(textarea.scrollHeight, minHeightPx);

    // Then measure width by preventing wrapping and adding buffer for accurate measurement
    textarea.style.whiteSpace = 'nowrap';
    textarea.style.width = 'auto';

    // Add small buffer (0.5rem) to prevent wrapping due to measurement precision issues
    let newWidthPx = Math.max(textarea.scrollWidth + remToPx(1), minWidthPx);

    // Apply max constraints
    if (maxWidthPx) {
      newWidthPx = Math.min(newWidthPx, maxWidthPx);
    }
    if (maxHeightPx) {
      newHeightPx = Math.min(newHeightPx, maxHeightPx);
    }

    // If width is constrained, recalculate height with that width
    if (maxWidthPx && (textarea.scrollWidth + remToPx(0.5)) > maxWidthPx - 4) {
      textarea.style.whiteSpace = '';
      textarea.style.width = `${newWidthPx}px`;
      textarea.style.height = 'auto';
      newHeightPx = Math.max(textarea.scrollHeight, minHeightPx);
      if (maxHeightPx) {
        newHeightPx = Math.min(newHeightPx, maxHeightPx);
      }
    }

    // Restore original styles before setting final dimensions
    textarea.style.width = originalWidth;
    textarea.style.height = originalHeight;
    textarea.style.whiteSpace = originalWhiteSpace;
    textarea.style.overflow = originalOverflow;

    // Convert back to rem for state
    setDimensions({ 
      width: pxToRem(newWidthPx), 
      height: pxToRem(newHeightPx) 
    });
  };

  useEffect(() => {
    adjustSize();
  }, [value, minWidth, minHeight, maxWidth, maxHeight]);

  const handleChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    onChange(e);
    // Use requestAnimationFrame for better timing
    requestAnimationFrame(adjustSize);
  };

  return (
    <span className="flex flex-col space-y-2">
      {label && (
        <label
          htmlFor={label.toLowerCase().replace(/\s+/g, '-')}
          className="text-sm font-medium text-gray-700"
        >
          {label}
        </label>
      )}
      <textarea
        {...props}
        ref={textareaRef}
        id={label?.toLowerCase().replace(/\s+/g, '-') || 'auto-size-textarea'}
        name={label?.toLowerCase().replace(/\s+/g, '-') || 'auto-size-textarea'}
        value={value}
        onChange={handleChange}
        placeholder={placeholder}
        className={`resize-none overflow-hidden border border-gray-300 rounded-md p-2 focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all duration-200 ${className}`}
        style={{
          width: `${dimensions.width}rem`,
          height: `${dimensions.height}rem`,
        }}
      />
    </span>
  );
}