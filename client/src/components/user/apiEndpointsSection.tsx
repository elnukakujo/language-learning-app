"use client";

import { useState } from "react";
import SectionCard from "./sectionCard";
import ConfirmDialog from "./confirmDialog";
import AutoWidthInput from "@/components/ui/input/autoWidthInput";
import SubmitButton from "@/components/ui/buttons/submitButton";
import { updateUserPreferences } from "@/api/userPreferences";
import { ApiEndpointConfig } from "@/interface/systemData/UserPreferences";

const TYPE_OPTIONS = ["text_gen", "tts", "both"] as const;
const TYPE_LABELS: Record<string, string> = {
    text_gen: "Text Gen",
    tts: "TTS",
    both: "Both",
};

export default function ApiEndpointsSection({
    prefId,
    endpoints: initial,
}: {
    prefId: string;
    endpoints: ApiEndpointConfig[];
}) {
    const [endpoints, setEndpoints] = useState<ApiEndpointConfig[]>(initial);
    const [showForm, setShowForm] = useState(false);
    const [editingIdx, setEditingIdx] = useState<number | null>(null);
    const [deleteIdx, setDeleteIdx] = useState<number | null>(null);
    const [saving, setSaving] = useState(false);

    // Form state
    const [name, setName] = useState("");
    const [apiType, setApiType] = useState<string>("text_gen");
    const [baseUrl, setBaseUrl] = useState("");
    const [apiKey, setApiKey] = useState("");
    const [model, setModel] = useState("");
    const [formError, setFormError] = useState("");

    const persist = async (updated: ApiEndpointConfig[]) => {
        setSaving(true);
        try {
            await updateUserPreferences(prefId, { ai_endpoints: updated });
            setEndpoints(updated);
        } finally {
            setSaving(false);
        }
    };

    const openCreate = () => {
        setName(""); setApiType("text_gen"); setBaseUrl(""); setApiKey(""); setModel("");
        setFormError(""); setEditingIdx(null); setShowForm(true);
    };

    const openEdit = (idx: number) => {
        const ep = endpoints[idx];
        setName(ep.name); setApiType(ep.api_type); setBaseUrl(ep.base_url ?? "");
        setApiKey(ep.api_key ?? ""); setModel(ep.model ?? "");
        setFormError(""); setEditingIdx(idx); setShowForm(true);
    };

    const handleSave = async (e: React.FormEvent) => {
        e.preventDefault();
        setFormError("");
        if (!name.trim()) { setFormError("Name is required"); return; }
        if (baseUrl && !baseUrl.startsWith("http://") && !baseUrl.startsWith("https://")) {
            setFormError("URL must start with http:// or https://");
            return;
        }
        const ep: ApiEndpointConfig = {
            name: name.trim(),
            api_type: apiType as ApiEndpointConfig["api_type"],
            base_url: baseUrl ? baseUrl.replace(/\/$/, "") : undefined,
            api_key: apiKey || undefined,
            model: model || undefined,
            is_active: editingIdx !== null ? endpoints[editingIdx].is_active : endpoints.length === 0,
        };
        const updated = editingIdx !== null
            ? endpoints.map((e, i) => i === editingIdx ? ep : e)
            : [...endpoints, ep];
        await persist(updated);
        setShowForm(false);
    };

    const handleDelete = async () => {
        if (deleteIdx === null) return;
        await persist(endpoints.filter((_, i) => i !== deleteIdx));
        setDeleteIdx(null);
    };

    const handleActivate = async (idx: number) => {
        const target = endpoints[idx];
        const types = target.api_type === "both" ? ["text_gen", "tts"] : [target.api_type];
        const updated = endpoints.map((e, i) => ({
            ...e,
            is_active: i === idx ? true
                : types.some((t) => (e.api_type === "both" || e.api_type === t) && e.is_active)
                    ? false : e.is_active,
        }));
        await persist(updated);
    };

    return (
        <SectionCard title="API Endpoints">
            <p className="text-sm opacity-60">
                Manage your LLM API connections. Only the active endpoint of each type is used.
            </p>

            {endpoints.length === 0 && !showForm && (
                <p className="text-sm opacity-40">No endpoints configured yet.</p>
            )}

            {endpoints.map((ep, idx) => (
                <div key={idx} className="flex items-center gap-2 flex-wrap py-2 border-b border-dashed border-[var(--color-border)] last:border-b-0">
                    <span className="font-medium">{ep.name}</span>
                    <span className="badge">{TYPE_LABELS[ep.api_type] ?? ep.api_type}</span>
                    {ep.base_url && (
                        <span className="text-sm opacity-60 truncate max-w-[200px]">{ep.base_url}</span>
                    )}
                    {ep.model && <span className="text-sm opacity-50">{ep.model}</span>}
                    {ep.is_active ? (
                        <span className="badge" style={{ background: "var(--color-primary)", color: "var(--color-primary-foreground)" }}>
                            Active
                        </span>
                    ) : (
                        <button type="button" className="btn btn-secondary text-xs" onClick={() => handleActivate(idx)} disabled={saving}>
                            Activate
                        </button>
                    )}
                    <div className="flex gap-1 ml-auto">
                        <button type="button" className="btn btn-secondary text-xs" onClick={() => openEdit(idx)} disabled={saving}>
                            Edit
                        </button>
                        <button type="button" className="btn btn-danger text-xs" onClick={() => setDeleteIdx(idx)} disabled={saving}>
                            Delete
                        </button>
                    </div>
                </div>
            ))}

            {showForm && (
                <form onSubmit={handleSave} className="flex flex-col gap-3 p-3 border border-dashed border-[var(--color-border)] rounded-lg">
                    <h4>{editingIdx !== null ? "Edit Endpoint" : "Add Endpoint"}</h4>
                    {formError && <p className="text-sm text-red-500">{formError}</p>}

                    <AutoWidthInput value={name} onChange={(e) => setName(e.target.value)}
                        placeholder="Name (e.g. Local Llama)" disabled={saving} />

                    <label className="flex flex-col gap-1">
                        <span className="text-sm opacity-70">Type</span>
                        <select className="input" value={apiType} onChange={(e) => setApiType(e.target.value)} disabled={saving}>
                            {TYPE_OPTIONS.map((t) => (
                                <option key={t} value={t}>{TYPE_LABELS[t]}</option>
                            ))}
                        </select>
                    </label>

                    <AutoWidthInput value={baseUrl} onChange={(e) => setBaseUrl(e.target.value)}
                        placeholder="Base URL (e.g. http://localhost:8080/v1)" disabled={saving} />
                    <AutoWidthInput value={apiKey} onChange={(e) => setApiKey(e.target.value)}
                        placeholder="API Key (optional)" type="password" disabled={saving} />
                    <AutoWidthInput value={model} onChange={(e) => setModel(e.target.value)}
                        placeholder="Model name (e.g. llama3)" disabled={saving} />

                    <div className="flex gap-2">
                        <SubmitButton isLoading={saving} />
                        <button type="button" className="btn btn-secondary" onClick={() => setShowForm(false)} disabled={saving}>
                            Cancel
                        </button>
                    </div>
                </form>
            )}

            {!showForm && (
                <button type="button" className="btn btn-secondary self-start" onClick={openCreate} disabled={saving}>
                    + Add Endpoint
                </button>
            )}

            {deleteIdx !== null && (
                <ConfirmDialog
                    message={`Delete "${endpoints[deleteIdx].name}"?`}
                    confirmLabel="Delete"
                    danger
                    onConfirm={handleDelete}
                    onCancel={() => setDeleteIdx(null)}
                />
            )}
        </SectionCard>
    );
}
