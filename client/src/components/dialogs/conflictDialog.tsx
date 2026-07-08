"use client";

import { createPortal } from "react-dom";
import ConflictError from "@/api/conflictError";

// Reuses the fixed-overlay createPortal pattern from buttons/deleteButton.tsx.
export default function ConflictDialog({
    error,
    onResolve,
    onCancel,
}: {
    error: ConflictError;
    onResolve: (choice: "keep" | "overwrite" | "merge") => void;
    onCancel: () => void;
}) {
    return createPortal(
        <div className="fixed inset-0 z-50 flex flex-col gap-4 items-center justify-center bg-black/80 backdrop-blur-sm p-4">
            <div className="bg-white rounded-lg p-6 max-w-lg w-full flex flex-col gap-4">
                <h3 className="text-lg font-semibold">
                    This {error.entityType} already exists
                </h3>
                <p className="text-sm text-gray-600">
                    A {error.entityType} with this value already exists for this language.
                    Choose how to resolve the conflict.
                </p>

                {error.diff.length > 0 && (
                    <table className="text-sm border-collapse w-full">
                        <thead>
                            <tr className="text-left border-b">
                                <th className="pr-4 py-1">Field</th>
                                <th className="pr-4 py-1">Existing</th>
                                <th className="py-1">Incoming</th>
                            </tr>
                        </thead>
                        <tbody>
                            {error.diff.map((field) => (
                                <tr key={field} className="border-b last:border-0">
                                    <td className="pr-4 py-1 font-medium">{field}</td>
                                    <td className="pr-4 py-1 text-gray-500">
                                        {String(error.existing[field] ?? "—")}
                                    </td>
                                    <td className="py-1">{String(error.incoming[field] ?? "—")}</td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                )}

                <div className="flex flex-row gap-2 justify-end flex-wrap">
                    <button
                        type="button"
                        onClick={onCancel}
                        className="border-2 rounded px-4 py-2"
                    >
                        Cancel
                    </button>
                    <button
                        type="button"
                        onClick={() => onResolve("keep")}
                        className="border-2 rounded px-4 py-2"
                        title="Discard what you entered, keep the existing entry as-is"
                    >
                        Keep Existing
                    </button>
                    <button
                        type="button"
                        onClick={() => onResolve("merge")}
                        className="border-2 rounded px-4 py-2"
                        title="Fill in only what's missing on the existing entry"
                    >
                        Merge
                    </button>
                    <button
                        type="button"
                        onClick={() => onResolve("overwrite")}
                        className="border-2 rounded px-4 py-2 bg-red-500 text-white"
                        title="Replace the existing entry with what you entered"
                    >
                        Overwrite
                    </button>
                </div>
            </div>
        </div>,
        document.body
    );
}
