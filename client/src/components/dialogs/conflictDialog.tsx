"use client";

import { useState } from "react";
import { createPortal } from "react-dom";
import ConflictError from "@/api/conflictError";

// error.diff never includes score/difficulty/dates (always keep the existing
// value) or tags/sources/media (combined automatically) — see
// DuplicateEntityError.EXCLUDED_FROM_DIFF server-side. Whatever's left is a
// real per-field decision for the user.

// Reuses the fixed-overlay createPortal pattern from buttons/deleteButton.tsx.
export default function ConflictDialog({
    error,
    onKeep,
    onOverwrite,
    onManualResolve,
    onCancel,
}: {
    error: ConflictError;
    onKeep: () => void;
    onOverwrite: () => void;
    onManualResolve: (resolvedFields: Record<string, string>) => void;
    onCancel: () => void;
}) {
    const editableFields = error.diff;

    const [values, setValues] = useState<Record<string, string>>(() => {
        const initial: Record<string, string> = {};
        for (const field of editableFields) {
            initial[field] = String(error.incoming[field] ?? error.existing[field] ?? "");
        }
        return initial;
    });

    return createPortal(
        <div className="fixed inset-0 z-50 flex flex-col gap-4 items-center justify-center bg-black/80 backdrop-blur-sm p-4">
            <div className="bg-white rounded-lg p-6 max-w-lg w-full flex flex-col gap-4 max-h-[85vh] overflow-y-auto">
                <h3 className="text-lg font-semibold">
                    This {error.entityType} already exists
                </h3>
                <p className="text-sm text-gray-600">
                    A {error.entityType} with this value already exists for this language.
                    Review each conflicting field below and decide what to keep.
                </p>

                {editableFields.length > 0 && (
                    <div className="flex flex-col gap-4">
                        {editableFields.map((field) => (
                            <div key={field} className="flex flex-col gap-1 border-b pb-3 last:border-0">
                                <span className="font-medium text-sm">{field}</span>
                                <div className="flex flex-row gap-2 text-xs text-gray-500">
                                    <button
                                        type="button"
                                        className="border rounded px-2 py-1 hover:bg-gray-100"
                                        onClick={() => setValues(v => ({ ...v, [field]: String(error.existing[field] ?? "") }))}
                                    >
                                        Use existing: &quot;{String(error.existing[field] ?? "—")}&quot;
                                    </button>
                                    <button
                                        type="button"
                                        className="border rounded px-2 py-1 hover:bg-gray-100"
                                        onClick={() => setValues(v => ({ ...v, [field]: String(error.incoming[field] ?? "") }))}
                                    >
                                        Use incoming: &quot;{String(error.incoming[field] ?? "—")}&quot;
                                    </button>
                                </div>
                                <input
                                    type="text"
                                    className="border border-gray-300 rounded px-2 py-1"
                                    value={values[field] ?? ""}
                                    onChange={(e) => setValues(v => ({ ...v, [field]: e.target.value }))}
                                    placeholder={`Type a value for ${field}`}
                                />
                            </div>
                        ))}
                    </div>
                )}

                <p className="text-xs text-gray-500">
                    Media, tags, and sources from both versions are combined automatically.
                    Score, difficulty, and dates keep the existing entry&apos;s values.
                </p>

                <div className="flex flex-row gap-2 justify-end flex-wrap pt-2">
                    <button type="button" onClick={onCancel} className="border-2 rounded px-4 py-2">
                        Cancel
                    </button>
                    <button
                        type="button"
                        onClick={onKeep}
                        className="border-2 rounded px-4 py-2"
                        title="Discard what you entered, keep the existing entry as-is"
                    >
                        Keep Existing
                    </button>
                    <button
                        type="button"
                        onClick={onOverwrite}
                        className="border-2 rounded px-4 py-2 bg-red-500 text-white"
                        title="Replace the existing entry with what you entered"
                    >
                        Overwrite
                    </button>
                    {editableFields.length > 0 && (
                        <button
                            type="button"
                            onClick={() => onManualResolve(values)}
                            className="border-2 rounded px-4 py-2 bg-blue-500 text-white"
                            title="Apply the values chosen/typed above"
                        >
                            Apply Chosen Values
                        </button>
                    )}
                </div>
            </div>
        </div>,
        document.body
    );
}
