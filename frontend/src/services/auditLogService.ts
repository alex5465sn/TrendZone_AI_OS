import { getData } from "./apiResponse";

export interface AuditLogItem {
    id: number;
    entity_type: string;
    entity_id: number | null;
    action: string;
    description: string;
    metadata: Record<string, any>;
    created_at: string | null;
}

export async function listAuditLogs(entityType?: string, limit = 100): Promise<AuditLogItem[]> {
    const params = new URLSearchParams();
    if (entityType) params.set("entity_type", entityType);
    params.set("limit", String(limit));
    return getData<AuditLogItem[]>(`/audit-logs?${params.toString()}`);
}

export async function listEntityTypes(): Promise<string[]> {
    return getData<string[]>("/audit-logs/entity-types");
}
