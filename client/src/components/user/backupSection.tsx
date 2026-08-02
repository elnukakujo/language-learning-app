"use client";

import { useEffect, useState } from "react";
import { createBackup, deleteBackup, listBackups, restoreBackup } from "@/api/backup";
import ConfirmDialog from "./confirmDialog";

type Backup = {
    filename: string;
    size_mb: number;
    created_at: string;
    is_latest: boolean;
};

export default function BackupSection() {
    const [backups, setBackups] = useState<Backup[]>([]);
    const [loading, setLoading] = useState(false);
    const [pendingRestore, setPendingRestore] = useState<string | null>(null);
    const [pendingDelete, setPendingDelete] = useState<string | null>(null);

    const refresh = async () => {
        const data = await listBackups();
        setBackups(data.backups || []);
    };

    useEffect(() => { refresh(); }, []);

    const handleCreate = async () => {
        setLoading(true);
        try {
            await createBackup();
            await refresh();
        } catch (error) {
            console.error("Failed to create backup:", error);
            alert("Failed to create backup.");
        } finally {
            setLoading(false);
        }
    };

    const handleRestore = async (filename: string) => {
        setLoading(true);
        try {
            await restoreBackup(filename);
            setPendingRestore(null);
        } catch (error) {
            console.error("Failed to restore backup:", error);
            alert("Failed to restore backup.");
        } finally {
            setLoading(false);
        }
    };

    const handleDelete = async (filename: string) => {
        try {
            await deleteBackup(filename);
            setPendingDelete(null);
            await refresh();
        } catch (error) {
            console.error("Failed to delete backup:", error);
            alert("Failed to delete backup.");
        }
    };

    return (
        <article className="flex flex-col gap-2 items-center">
            <h3>Backups</h3>
            <p className="text-sm text-muted">Up to 10 most recent backups are kept automatically.</p>
            <button type="button" onClick={handleCreate} disabled={loading} className="btn btn-primary">
                {loading ? "Working..." : "Create Backup"}
            </button>
            <ul className="flex flex-col gap-2 w-full max-w-md">
                {backups.map((b) => (
                    <li key={b.filename} className="flex items-center justify-between gap-2 rounded border border-border px-3 py-2 text-sm">
                        <div className="flex flex-col">
                            <span>{new Date(b.created_at).toLocaleString()}{b.is_latest ? " (latest)" : ""}</span>
                            <span className="text-muted">{b.size_mb} MB</span>
                        </div>
                        <div className="flex gap-2">
                            <button type="button" onClick={() => setPendingRestore(b.filename)} disabled={loading} className="btn btn-secondary">
                                Restore
                            </button>
                            <button type="button" onClick={() => setPendingDelete(b.filename)} disabled={loading || backups.length <= 1} className="btn btn-danger">
                                Delete
                            </button>
                        </div>
                    </li>
                ))}
                {backups.length === 0 && <li className="text-sm text-muted">No backups yet.</li>}
            </ul>

            {pendingRestore && (
                <ConfirmDialog
                    message={`Restore database from "${pendingRestore}"? This will overwrite current data.`}
                    confirmLabel="Confirm Restore"
                    danger
                    onConfirm={() => handleRestore(pendingRestore)}
                    onCancel={() => setPendingRestore(null)}
                />
            )}

            {pendingDelete && (
                <ConfirmDialog
                    message={`Delete backup "${pendingDelete}"?`}
                    confirmLabel="Delete"
                    danger
                    onConfirm={() => handleDelete(pendingDelete)}
                    onCancel={() => setPendingDelete(null)}
                />
            )}
        </article>
    );
}
