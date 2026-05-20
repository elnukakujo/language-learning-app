"use client";

import { useEffect, useMemo, useRef, useState } from "react";
import { getAllUserTags, addTagToElement, removeTagFromElement } from "@/api/tag";
import TagForm from "@/components/forms/entityForms/tagForm";
import { createPortal } from "react-dom";
import type Tag from "@/interface/systemData/Tag";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faTimes, faPlus } from "@fortawesome/free-solid-svg-icons";
import { getCurrentUserId } from "@/utils/user_cookie";

interface TagSelectorProps {
  selectedTagIds: string[];
  onTagsChange: (tagIds: string[]) => void;
  elementId: string;
  disabled?: boolean;
}

function normalizeTags(payload: unknown): Tag[] {
  if (Array.isArray(payload)) return payload as Tag[];
  if (payload && typeof payload === "object") {
    const wrapped = payload as { tags?: Tag[] };
    if (Array.isArray(wrapped.tags)) return wrapped.tags;
  }
  return [];
}

export default function TagSelector({
  selectedTagIds,
  onTagsChange,
  elementId,
  disabled = false
}: TagSelectorProps) {
  const [allTags, setAllTags] = useState<Tag[]>([]);
  const [searchInput, setSearchInput] = useState("");
  const [isOpen, setIsOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [error, setError] = useState("");
  // Track which tag IDs are currently mid-request to show a loading state on them
  const [pendingTagIds, setPendingTagIds] = useState<Set<string>>(new Set());
  const containerRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const fetchTags = async () => {
    setIsLoading(true);
    try {
      const currentUserId: string | null = await getCurrentUserId();
      const response = await getAllUserTags(currentUserId!);
      setAllTags(normalizeTags(response));
    } catch (err) {
      console.error("Failed to fetch tags:", err);
      setError("Failed to load tags");
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    let active = true;
    fetchTags();
    return () => { active = false; };
  }, []);

  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (containerRef.current && !containerRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const selectedTags = useMemo(
    () => allTags.filter((tag) => selectedTagIds.includes(tag.id)),
    [allTags, selectedTagIds]
  );

  const trimmedInput = searchInput.trim();

  const filteredTags = useMemo(() => {
    const query = trimmedInput.toLowerCase();
    return allTags.filter(
      (tag) =>
        !selectedTagIds.includes(tag.id) &&
        (!query || tag.name.toLowerCase().includes(query))
    );
  }, [allTags, trimmedInput, selectedTagIds]);

  const canCreateTag = useMemo(() => {
    if (!trimmedInput || disabled) return false;
    return !allTags.some(
      (tag) => tag.name.trim().toLowerCase() === trimmedInput.toLowerCase()
    );
  }, [allTags, disabled, trimmedInput]);

  const setPending = (tagId: string, pending: boolean) => {
    setPendingTagIds((prev) => {
      const next = new Set(prev);
      pending ? next.add(tagId) : next.delete(tagId);
      return next;
    });
  };

  const handleSelectTag = async (tag: Tag) => {
    if (selectedTagIds.includes(tag.id) || pendingTagIds.has(tag.id)) return;

    // Optimistic update
    onTagsChange([...selectedTagIds, tag.id]);
    setSearchInput("");
    setIsOpen(false);
    inputRef.current?.focus();

    if (!elementId) return; // If it is part of a create form the add logic will be handled in the form submission

    setPending(tag.id, true);
    console.log(`Adding tag "${tag.name}" with ID ${tag.id} to element ${elementId}...`);
    try {
      await addTagToElement(tag.id, elementId);
    } catch (err) {
      console.error(`Failed to add tag "${tag.name}":`, err);
      setError(`Failed to add tag "${tag.name}"`);
      // Roll back
      onTagsChange(selectedTagIds.filter((id) => id !== tag.id));
    } finally {
      setPending(tag.id, false);
    }
  };

  const handleRemoveTag = async (tag: Tag) => {
    if (pendingTagIds.has(tag.id)) return;

    // Optimistic update
    onTagsChange(selectedTagIds.filter((id) => id !== tag.id));

    if (!elementId) return; // If it is part of a create form the remove logic will be handled in the form submission

    setPending(tag.id, true);
    console.log(`Removing tag "${tag.name}" with ID ${tag.id} from element ${elementId}...`);

    try {
      await removeTagFromElement(tag.id, elementId);
    } catch (err) {
      console.error(`Failed to remove tag "${tag.name}":`, err);
      setError(`Failed to remove tag "${tag.name}"`);
      // Roll back
      onTagsChange([...selectedTagIds, tag.id]);
    } finally {
      setPending(tag.id, false);
    }
  };

  const handleCloseCreateModal = async () => {
    setShowCreateModal(false);
    await fetchTags();
  };

  return (
    <>
      <section ref={containerRef} className="flex w-full max-w-md flex-col gap-1.5">
        <label className="text-xs font-medium uppercase tracking-wide text-gray-500">
          Tags
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
            {selectedTags.map((tag) => {
              const isPending = pendingTagIds.has(tag.id);
              return (
                <span
                  key={tag.id}
                  className={`inline-flex items-center gap-1.5 rounded-full pl-2 pr-1 py-0.5 text-xs font-medium transition-opacity
                    ${isPending ? "opacity-50" : "opacity-100"}
                    bg-blue-50 text-blue-800`}
                >
                  {tag.color && (
                    <span className="h-2 w-2 flex-shrink-0 rounded-full" style={{ backgroundColor: tag.color }} />
                  )}
                  {tag.name}
                  <button
                    type="button"
                    onClick={(e) => { e.stopPropagation(); handleRemoveTag(tag); }}
                    disabled={disabled || isPending}
                    className="flex h-4 w-4 items-center justify-center rounded-full text-blue-500 transition-colors hover:bg-blue-200 hover:text-blue-900 disabled:pointer-events-none disabled:opacity-40"
                    aria-label={`Remove ${tag.name}`}
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
                placeholder={selectedTags.length === 0 ? "Search or add tags…" : ""}
                disabled={disabled}
                className="min-w-[120px] flex-1 bg-transparent text-sm text-gray-700 placeholder:text-gray-400 outline-none"
              />
            )}
          </div>

          {isOpen && !isLoading && (
            <div className="absolute left-0 right-0 top-full z-50 mt-1 max-h-52 overflow-y-auto rounded-lg border border-gray-200 bg-white shadow-md">
              {filteredTags.length > 0
                ? filteredTags.map((tag) => (
                    <button
                      key={tag.id}
                      type="button"
                      onMouseDown={(e) => e.preventDefault()}
                      onClick={() => handleSelectTag(tag)}
                      className="flex w-full items-center gap-2.5 px-3 py-2 text-left text-sm transition-colors hover:bg-blue-50"
                    >
                      {tag.color && (
                        <span className="h-2.5 w-2.5 flex-shrink-0 rounded-full" style={{ backgroundColor: tag.color }} />
                      )}
                      <span className="text-gray-700">{tag.name}</span>
                    </button>
                  ))
                : !canCreateTag && (
                    <p className="px-3 py-2 text-sm text-gray-400">No matching tags</p>
                  )}

              {canCreateTag && (
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
                <h2 className="text-base font-medium text-gray-800">Create tag</h2>
                <button
                  type="button"
                  onClick={handleCloseCreateModal}
                  className="text-gray-400 transition-colors hover:text-gray-700"
                >
                  <FontAwesomeIcon icon={faTimes} />
                </button>
              </div>
              <TagForm tag={{ name: searchInput }} navDisabled={true} onSuccess={handleCloseCreateModal} />
            </div>
          </section>,
          document.body
        )}
    </>
  );
}