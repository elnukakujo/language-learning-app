"use client";

import { useEffect, useMemo, useRef, useState } from "react";
import { getAllUserSources, addSourceToElement, removeSourceFromElement } from "@/api";
import SourceForm from "@/components/forms/entityForms/sourceForm";
import { createPortal } from "react-dom";
import type Source from "@/interface/systemData/Source";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faTimes, faPlus } from "@fortawesome/free-solid-svg-icons";

interface SourceSelectorProps {
  selectedSourceIds: string[];
  onSourcesChange: (sourceIds: string[]) => void;
  elementId: string;
  disabled?: boolean;
  userId?: string;
}

function normalizeSources(payload: unknown): Source[] {
  if (Array.isArray(payload)) return payload as Source[];
  if (payload && typeof payload === "object") {
    const wrapped = payload as { sources?: Source[] };
    if (Array.isArray(wrapped.sources)) return wrapped.sources;
  }
  return [];
}

export default function SourceSelector({
  selectedSourceIds,
  onSourcesChange,
  elementId,
  disabled = false,
  userId = "user_U0",
}: SourceSelectorProps) {
  const [allSources, setAllSources] = useState<Source[]>([]);
  const [searchInput, setSearchInput] = useState("");
  const [isOpen, setIsOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [error, setError] = useState("");
  // Track which source IDs are currently mid-request to show a loading state on them
  const [pendingSourceIds, setPendingSourceIds] = useState<Set<string>>(new Set());
  const containerRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const fetchSources = async () => {
    setIsLoading(true);
    try {
      const response = await getAllUserSources(userId);
      setAllSources(normalizeSources(response));
    } catch (err) {
      console.error("Failed to fetch sources:", err);
      setError("Failed to load sources");
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    let active = true;
    getAllUserSources(userId)
      .then((response) => { if (active) setAllSources(normalizeSources(response)); })
      .catch(() => { if (active) setError("Failed to load sources"); })
      .finally(() => { if (active) setIsLoading(false); });
    return () => { active = false; };
  }, [userId]);

  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (containerRef.current && !containerRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const selectedSources = useMemo(
    () => allSources.filter((source) => selectedSourceIds.includes(source.id)),
    [allSources, selectedSourceIds]
  );

  const trimmedInput = searchInput.trim();

  const filteredSources = useMemo(() => {
    const query = trimmedInput.toLowerCase();
    return allSources.filter(
      (source) =>
        !selectedSourceIds.includes(source.id) &&
        (!query || source.title.toLowerCase().includes(query))
    );
  }, [allSources, trimmedInput, selectedSourceIds]);

  const canCreateSource = useMemo(() => {
    if (!trimmedInput || disabled) return false;
    return !allSources.some(
      (source) => source.title.trim().toLowerCase() === trimmedInput.toLowerCase()
    );
  }, [allSources, disabled, trimmedInput]);

  const setPending = (sourceId: string, pending: boolean) => {
    setPendingSourceIds((prev) => {
      const next = new Set(prev);
      pending ? next.add(sourceId) : next.delete(sourceId);
      return next;
    });
  };

  const handleSelectSource = async (source: Source) => {
    if (selectedSourceIds.includes(source.id) || pendingSourceIds.has(source.id)) return;

    // Optimistic update
    onSourcesChange([...selectedSourceIds, source.id]);
    setSearchInput("");
    setIsOpen(false);
    inputRef.current?.focus();

    if (!elementId) return; // If it is part of a create form the add logic will be handled in the form submission

    setPending(source.id, true);
    console.log(`Adding source "${source.title}" with ID ${source.id} to element ${elementId}...`);
    try {
      await addSourceToElement(source.id, elementId);
    } catch (err) {
      console.error(`Failed to add source "${source.title}":`, err);
      setError(`Failed to add source "${source.title}"`);
      // Roll back
      onSourcesChange(selectedSourceIds.filter((id) => id !== source.id));
    } finally {
      setPending(source.id, false);
    }
  };

  const handleRemoveSource = async (source: Source) => {
    if (pendingSourceIds.has(source.id)) return;

    // Optimistic update
    onSourcesChange(selectedSourceIds.filter((id) => id !== source.id));

    if (!elementId) return; // If it is part of a create form the remove logic will be handled in the form submission

    setPending(source.id, true);
    console.log(`Removing source "${source.title}" with ID ${source.id} from element ${elementId}...`);

    try {
      await removeSourceFromElement(source.id, elementId);
    } catch (err) {
      console.error(`Failed to remove source "${source.title}":`, err);
      setError(`Failed to remove source "${source.title}"`);
      // Roll back
      onSourcesChange([...selectedSourceIds, source.id]);
    } finally {
      setPending(source.id, false);
    }
  };

  const handleCloseCreateModal = async () => {
    setShowCreateModal(false);
    await fetchSources();
  };

  return (
    <>
      <section ref={containerRef} className="flex w-full max-w-md flex-col gap-1.5">
        <label className="text-xs font-medium uppercase tracking-wide text-gray-500">
          Sources
        </label>

        {error && (
          <p className="rounded-md bg-red-50 px-3 py-2 text-sm text-red-600">{error}</p>
        )}

        <div className="relative">
          <div
            className={`
              flex min-h-10 flex-wrap items-center gap-1.5 rounded-lg border px-2 py-1.5 transition-colors
              ${disabled ? "bg-gray-50 border-gray-200" : "bg-white border-gray-300 focus-within:border-blue-400 focus-within:ring-2 focus-within:ring-blue-100"}
            `}
            onClick={() => { if (!disabled) { setIsOpen(true); inputRef.current?.focus(); } }}
          >
            {selectedSources.map((source) => {
              const isPending = pendingSourceIds.has(source.id);
              return (
                <span
                  key={source.id}
                  className={`inline-flex items-center gap-1.5 rounded-full pl-2 pr-1 py-0.5 text-xs font-medium transition-opacity
                    ${isPending ? "opacity-50" : "opacity-100"}
                    bg-blue-50 text-blue-800`}
                >
                  {source.title}
                  <button
                    type="button"
                    onClick={(e) => { e.stopPropagation(); handleRemoveSource(source); }}
                    disabled={disabled || isPending}
                    className="flex h-4 w-4 items-center justify-center rounded-full text-blue-500 transition-colors hover:bg-blue-200 hover:text-blue-900 disabled:pointer-events-none disabled:opacity-40"
                    aria-label={`Remove ${source.title}`}
                  >
                    <FontAwesomeIcon icon={faTimes} className="text-[10px]" />
                  </button>
                </span>
              );
            })}

            {isLoading ? (
              <span className="px-1 text-sm text-gray-400">Loading…</span>
            ) : (
              <input
                ref={inputRef}
                type="text"
                value={searchInput}
                onChange={(e) => { setSearchInput(e.target.value); setIsOpen(true); }}
                onFocus={() => setIsOpen(true)}
                placeholder={selectedSources.length === 0 ? "Search or add sources…" : ""}
                disabled={disabled}
                className="min-w-[120px] flex-1 bg-transparent text-sm text-gray-700 placeholder:text-gray-400 outline-none"
              />
            )}
          </div>

          {isOpen && !isLoading && (
            <div className="absolute left-0 right-0 top-full z-50 mt-1 max-h-52 overflow-y-auto rounded-lg border border-gray-200 bg-white shadow-md">
              {filteredSources.length > 0
                ? filteredSources.map((source) => (
                    <button
                      key={source.id}
                      type="button"
                      onMouseDown={(e) => e.preventDefault()}
                      onClick={() => handleSelectSource(source)}
                      className="flex w-full items-center gap-2.5 px-3 py-2 text-left text-sm transition-colors hover:bg-blue-50"
                    >
                      <span className="text-gray-700">{source.title}</span>
                    </button>
                  ))
                : !canCreateSource && (
                    <p className="px-3 py-2 text-sm text-gray-400">No matching sources</p>
                  )}

              {canCreateSource && (
                <button
                  type="button"
                  onMouseDown={(e) => e.preventDefault()}
                  onClick={() => { setIsOpen(false); setShowCreateModal(true); }}
                  className="flex w-full items-center gap-2 border-t border-gray-100 px-3 py-2 text-left text-sm text-blue-600 transition-colors hover:bg-blue-50"
                >
                  <FontAwesomeIcon icon={faPlus} className="text-xs" />
                  <span>Create &ldquo;{trimmedInput}&rdquo;</span>
                </button>
              )}
            </div>
          )}
        </div>
      </section>

      {showCreateModal &&
        createPortal(
          <section
            className="fixed inset-0 z-50 flex items-center justify-center bg-black/40"
            onClick={handleCloseCreateModal}
			      onSubmit={(e) => e.stopPropagation()}
          >
            <div
              className="w-full max-w-lg rounded-xl bg-white p-6 shadow-xl"
              onClick={(e) => e.stopPropagation()}
            >
              <div className="mb-4 flex items-center justify-between">
                <h2 className="text-base font-medium text-gray-800">Create source</h2>
                <button
                  type="button"
                  onClick={handleCloseCreateModal}
                  className="text-gray-400 transition-colors hover:text-gray-700"
                >
                  <FontAwesomeIcon icon={faTimes} />
                </button>
              </div>
              <SourceForm source={{ title: searchInput }} navDisabled={true} onSuccess={handleCloseCreateModal} />
            </div>
          </section>,
          document.body
        )}
    </>
  );
}