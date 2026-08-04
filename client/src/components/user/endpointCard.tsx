"use client";

import { useState } from "react";
import { Eye, EyeOff, Copy, Check, ChevronDown, ChevronUp, ArrowUp, ArrowDown } from "lucide-react";
import ConfirmDialog from "./confirmDialog";
import { ApiEndpointConfig } from "@/interface/systemData/UserPreferences";

const PROVIDER_OPTIONS = [
  { value: "openai_compatible", label: "OpenAI Compatible" },
  { value: "deepseek", label: "DeepSeek" },
  { value: "anthropic", label: "Anthropic" },
  { value: "ollama", label: "Ollama" },
  { value: "custom", label: "Custom" },
] as const;

const TYPE_OPTIONS = [
  { value: "text_gen", label: "Text Generation" },
  { value: "tts", label: "Text-to-Speech" },
  { value: "both", label: "Both" },
] as const;

const TYPE_LABELS: Record<string, string> = {
  text_gen: "Text Gen",
  tts: "TTS",
  both: "Both",
};

export default function EndpointCard({
  endpoint,
  index,
  total,
  onUpdate,
  onDelete,
  onMoveUp,
  onMoveDown,
  onTestConnection,
  testResult,
  disabled,
}: {
  endpoint: ApiEndpointConfig;
  index: number;
  total: number;
  onUpdate: (updated: ApiEndpointConfig) => void;
  onDelete: () => void;
  onMoveUp: () => void;
  onMoveDown: () => void;
  onTestConnection: () => void;
  testResult: { ok: boolean; ms?: number; error?: string } | null;
  disabled: boolean;
}) {
  const [expanded, setExpanded] = useState(false);
  const [showKey, setShowKey] = useState(false);
  const [copied, setCopied] = useState(false);
  const [confirmDelete, setConfirmDelete] = useState(false);

  const handleCopy = async () => {
    if (!endpoint.api_key) return;
    try {
      await navigator.clipboard.writeText(endpoint.api_key);
      setCopied(true);
      setTimeout(() => setCopied(false), 1500);
    } catch {
      // clipboard may be denied — silently ignore
    }
  };

  const statusBadge = testResult
    ? testResult.ok
      ? { label: `Connected — ${testResult.ms} ms`, color: "var(--color-success)", bg: "var(--color-success)" }
      : { label: "Error", color: "var(--color-danger)", bg: "var(--color-danger)" }
    : endpoint.base_url
      ? { label: "Untested", color: "var(--color-muted)", bg: "var(--color-muted)" }
      : { label: "Unconfigured", color: "var(--color-muted)", bg: "var(--color-muted)" };

  return (
    <div className="endpoint-card card">
      {/* Collapsed header */}
      <div className="flex items-center gap-2 flex-wrap">
        <button
          type="button"
          className="flex items-center gap-2 flex-1 min-w-0 text-left"
          onClick={() => setExpanded(!expanded)}
          aria-expanded={expanded}
        >
          {expanded ? <ChevronUp size={16} className="shrink-0 opacity-50" /> : <ChevronDown size={16} className="shrink-0 opacity-50" />}
          <span className="font-medium truncate">{endpoint.name || "Unnamed endpoint"}</span>
          <span className="badge">{TYPE_LABELS[endpoint.api_type] ?? endpoint.api_type}</span>
        </button>

        <span
          className="badge text-xs"
          style={{ background: statusBadge.bg, color: "#fffbf3" }}
        >
          {statusBadge.label}
        </span>

        {endpoint.is_active && (
          <span className="badge" style={{ background: "var(--color-primary)", color: "var(--color-primary-foreground)" }}>
            Active
          </span>
        )}

        {/* Reorder */}
        <div className="flex gap-0.5 ml-auto">
          <button
            type="button"
            className="btn btn-secondary text-xs px-1.5"
            onClick={onMoveUp}
            disabled={disabled || index === 0}
            aria-label="Move up"
          >
            <ArrowUp size={14} />
          </button>
          <button
            type="button"
            className="btn btn-secondary text-xs px-1.5"
            onClick={onMoveDown}
            disabled={disabled || index === total - 1}
            aria-label="Move down"
          >
            <ArrowDown size={14} />
          </button>
        </div>
      </div>

      {/* Expanded form */}
      {expanded && (
        <div className="flex flex-col gap-3 pt-3 mt-3 border-t border-dashed border-[var(--color-border)]">
          {/* Display Name */}
          <label className="flex flex-col gap-1">
            <span className="text-sm opacity-70">Display Name</span>
            <input
              className="input"
              type="text"
              value={endpoint.name}
              onChange={(e) => onUpdate({ ...endpoint, name: e.target.value })}
              placeholder="e.g. Local Llama"
              disabled={disabled}
            />
          </label>

          {/* Provider Type */}
          <label className="flex flex-col gap-1">
            <span className="text-sm opacity-70">Provider</span>
            <select
              className="input"
              value={(endpoint as any).provider ?? "custom"}
              onChange={(e) => onUpdate({ ...endpoint, provider: e.target.value } as any)}
              disabled={disabled}
            >
              {PROVIDER_OPTIONS.map(({ value, label }) => (
                <option key={value} value={value}>{label}</option>
              ))}
            </select>
            {// TODO: persist provider_type to ApiEndpointConfig + backend schema
            }
          </label>

          {/* API Type / Purpose */}
          <label className="flex flex-col gap-1">
            <span className="text-sm opacity-70">Purpose</span>
            <select
              className="input"
              value={endpoint.api_type}
              onChange={(e) => onUpdate({ ...endpoint, api_type: e.target.value as ApiEndpointConfig["api_type"] })}
              disabled={disabled}
            >
              {TYPE_OPTIONS.map(({ value, label }) => (
                <option key={value} value={value}>{label}</option>
              ))}
            </select>
          </label>

          {/* Voice (TTS only) */}
          {(endpoint.api_type === "tts" || endpoint.api_type === "both") && (
            <label className="flex flex-col gap-1">
              <span className="text-sm opacity-70">Voice</span>
              <input
                className="input"
                type="text"
                value={endpoint.voice ?? ""}
                onChange={(e) => onUpdate({ ...endpoint, voice: e.target.value || undefined })}
                placeholder="alloy (OpenAI) or en_f (Kokoro)"
                disabled={disabled}
              />
              <span className="text-xs opacity-40">Kokoro uses codes like en_f, ja_f, fr_f — leave blank for OpenAI default.</span>
            </label>
          )}

          {/* Base URL */}
          <label className="flex flex-col gap-1">
            <span className="text-sm opacity-70">Base URL</span>
            <input
              className="input"
              type="url"
              value={endpoint.base_url ?? ""}
              onChange={(e) => onUpdate({ ...endpoint, base_url: e.target.value || undefined })}
              placeholder="https://api.openai.com/v1"
              disabled={disabled}
            />
            <span className="text-xs opacity-40">The API root — the app appends /audio/speech or /chat/completions automatically.</span>
          </label>

          {/* Model + Test Connection */}
          <label className="flex flex-col gap-1">
            <span className="text-sm opacity-70">Model Name</span>
            <div className="flex gap-2">
              <input
                className="input flex-1"
                type="text"
                value={endpoint.model ?? ""}
                onChange={(e) => onUpdate({ ...endpoint, model: e.target.value || undefined })}
                placeholder="e.g. gpt-4o"
                disabled={disabled}
              />
              <button
                type="button"
                className="btn btn-secondary text-xs shrink-0"
                onClick={onTestConnection}
                disabled={disabled}
              >
                Test connection
              </button>
            </div>
            {testResult && (
              <span
                className={`text-xs ${testResult.ok ? "" : ""}`}
                style={{ color: testResult.ok ? "var(--color-success)" : "var(--color-danger)" }}
              >
                {testResult.ok
                  ? `✓ Connected — ${testResult.ms} ms`
                  : `✗ ${testResult.error ?? "Connection failed"}`}
              </span>
            )}
          </label>

          {/* API Key */}
          <label className="flex flex-col gap-1">
            <span className="text-sm opacity-70">API Key</span>
            <div className="relative">
              <input
                className="input pr-20"
                type={showKey ? "text" : "password"}
                value={endpoint.api_key ?? ""}
                onChange={(e) => onUpdate({ ...endpoint, api_key: e.target.value || undefined })}
                placeholder="sk-..."
                disabled={disabled}
              />
              <div className="absolute right-1.5 top-1/2 -translate-y-1/2 flex gap-0.5">
                <button
                  type="button"
                  className="p-1 rounded opacity-50 hover:opacity-80"
                  onClick={() => setShowKey(!showKey)}
                  tabIndex={-1}
                  aria-label={showKey ? "Hide API key" : "Show API key"}
                >
                  {showKey ? <EyeOff size={14} /> : <Eye size={14} />}
                </button>
                <button
                  type="button"
                  className="p-1 rounded opacity-50 hover:opacity-80"
                  onClick={handleCopy}
                  tabIndex={-1}
                  aria-label="Copy API key"
                  disabled={!endpoint.api_key}
                >
                  {copied ? <Check size={14} color="var(--color-success)" /> : <Copy size={14} />}
                </button>
              </div>
            </div>
          </label>

          {/* Actions */}
          <div className="flex items-center gap-2 pt-1">
            {!endpoint.is_active ? (
              <button
                type="button"
                className="btn btn-secondary text-xs"
                onClick={() => onUpdate({ ...endpoint, is_active: true })}
                disabled={disabled}
              >
                Activate
              </button>
            ) : (
              <button
                type="button"
                className="btn btn-secondary text-xs"
                onClick={() => onUpdate({ ...endpoint, is_active: false })}
                disabled={disabled}
              >
                Deactivate
              </button>
            )}
            <button
              type="button"
              className="btn btn-danger text-xs ml-auto"
              onClick={() => setConfirmDelete(true)}
              disabled={disabled}
            >
              Delete
            </button>
          </div>
        </div>
      )}

      {confirmDelete && (
        <ConfirmDialog
          message={`Delete "${endpoint.name || "Unnamed endpoint"}"?`}
          confirmLabel="Delete"
          danger
          onConfirm={onDelete}
          onCancel={() => setConfirmDelete(false)}
        />
      )}
    </div>
  );
}
