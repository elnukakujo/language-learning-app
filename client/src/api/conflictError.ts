// Thrown by create*() calls when the server responds 409 (duplicate word/character
// for the language). Callers catch this specifically to drive a ConflictDialog
// instead of treating it as a generic failure.
export default class ConflictError extends Error {
  entityType: string;
  existing: Record<string, unknown>;
  incoming: Record<string, unknown>;
  diff: string[];

  constructor(payload: {
    entity_type: string;
    existing: Record<string, unknown>;
    incoming: Record<string, unknown>;
    diff: string[];
  }) {
    super(`Duplicate ${payload.entity_type}: ${payload.existing.id}`);
    this.name = "ConflictError";
    this.entityType = payload.entity_type;
    this.existing = payload.existing;
    this.incoming = payload.incoming;
    this.diff = payload.diff;
  }
}

export async function throwIfConflict(res: Response): Promise<void> {
  if (res.status !== 409) return;
  const body = await res.json();
  throw new ConflictError(body);
}
