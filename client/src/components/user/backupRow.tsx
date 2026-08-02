"use client";

import { useState } from "react";
import { Download, RotateCcw, Trash2 } from "lucide-react";
import ConfirmDialog from "./confirmDialog";

export type Backup = {
  filename: string;
  size_mb: number;
  created_at: string;
  is_latest: boolean;
};

export default function BackupRow({
  backup,
  onRestore,
  onDelete,
  disabled,
}: {
  backup: Backup;
  onRestore: () => void;
  onDelete: () => void;
  disabled: boolean;
}) {
  const [confirmRestore, setConfirmRestore] = useState(false);
  const [confirmDelete, setConfirmDelete] = useState(false);

  const type = backup.filename.includes("auto") ? "Auto" : "Manual"; // ponytail: heuristic, TODO: add type field to backup API response
  const date = new Date(backup.created_at).toLocaleString();

  return (
    <div className="backup-row flex items-center justify-between gap-3 py-3 px-1 border-b border-dashed border-[var(--color-border)] last:border-b-0">
      <div className="flex flex-col min-w-0">
        <div className="flex items-center gap-2">
          <span className="font-mono text-sm truncate" style={{ fontFamily: "var(--font-mono)" }}>
            {backup.filename}
          </span>
          {backup.is_latest && (
            <span className="badge" style={{ background: "var(--color-success)", color: "#fffbf3" }}>
              Latest
            </span>
          )}
        </div>
        <div className="flex items-center gap-2 text-xs opacity-50">
          <span>{date}</span>
          <span aria-hidden="true">·</span>
          <span>{backup.size_mb} MB</span>
          <span aria-hidden="true">·</span>
          <span className="badge">{type}</span>
        </div>
      </div>

      <div className="flex gap-1 shrink-0">
        <button
          type="button"
          className="btn btn-secondary text-xs"
          onClick={() => setConfirmRestore(true)}
          disabled={disabled}
        >
          <RotateCcw size={14} />
          <span className="hidden sm:inline">Restore</span>
        </button>
        <button
          type="button"
          className="btn btn-secondary text-xs"
          disabled
          title="Not yet implemented"
        >
          <Download size={14} />
          <span className="hidden sm:inline">Download</span>
        </button>
        <button
          type="button"
          className="btn btn-danger text-xs"
          onClick={() => setConfirmDelete(true)}
          disabled={disabled}
        >
          <Trash2 size={14} />
          <span className="hidden sm:inline">Delete</span>
        </button>
      </div>

      {confirmRestore && (
        <ConfirmDialog
          message={`Restore database from "${backup.filename}"? This will overwrite current data.`}
          confirmLabel="Confirm Restore"
          danger
          onConfirm={() => { setConfirmRestore(false); onRestore(); }}
          onCancel={() => setConfirmRestore(false)}
        />
      )}

      {confirmDelete && (
        <ConfirmDialog
          message={`Delete backup "${backup.filename}"?`}
          confirmLabel="Delete"
          danger
          onConfirm={() => { setConfirmDelete(false); onDelete(); }}
          onCancel={() => setConfirmDelete(false)}
        />
      )}
    </div>
  );
}
