class DuplicateEntityError(Exception):
    """Raised by a create() call that found an existing row and wasn't told
    how to resolve it (no on_conflict given). Callers at the route layer
    catch this and return HTTP 409 with existing/incoming/diff so the client
    can offer keep / overwrite / a per-field manual resolution instead of
    silently upserting.
    """

    # Never part of the conflict: score/difficulty/dates/status always keep
    # the existing value regardless of on_conflict (update() already excludes
    # them from what it writes); tags/sources/media are stacked (unioned),
    # not decided field-by-field, so they're excluded from `diff` too.
    EXCLUDED_FROM_DIFF = {
        "score", "difficulty", "created_at", "last_seen_at", "status",
        "tags", "sources", "image_files", "audio_files",
    }

    def __init__(self, entity_type: str, existing: dict, incoming: dict):
        self.entity_type = entity_type
        self.existing = existing
        self.incoming = incoming
        self.diff = sorted(
            key
            for key, incoming_val in incoming.items()
            if key in existing
            and key not in self.EXCLUDED_FROM_DIFF
            and incoming_val not in (None, "")
            and existing[key] != incoming_val
        )
        super().__init__(f"Duplicate {entity_type}: existing id={existing.get('id')}")
