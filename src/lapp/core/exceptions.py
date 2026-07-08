class DuplicateEntityError(Exception):
    """Raised by a create() call that found an existing row and wasn't told
    how to resolve it (no on_conflict given). Callers at the route layer
    catch this and return HTTP 409 with existing/incoming/diff so the client
    can offer keep / overwrite / merge instead of silently upserting.
    """

    def __init__(self, entity_type: str, existing: dict, incoming: dict):
        self.entity_type = entity_type
        self.existing = existing
        self.incoming = incoming
        self.diff = sorted(
            key
            for key, incoming_val in incoming.items()
            if key in existing and incoming_val not in (None, "") and existing[key] != incoming_val
        )
        super().__init__(f"Duplicate {entity_type}: existing id={existing.get('id')}")
