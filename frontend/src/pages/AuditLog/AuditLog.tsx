import { useEffect, useState } from "react";

import {
    Box,
    Typography,
    Chip,
    CircularProgress,
    Alert,
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow,
    Paper,
    MenuItem,
    TextField,
} from "@mui/material";

import { listAuditLogs, listEntityTypes, type AuditLogItem } from "../../services/auditLogService";

const actionColors: Record<string, string> = {
    CREATE: "#10B981",
    UPDATE: "#3B82F6",
    DELETE: "#EF4444",
    MOVE: "#F59E0B",
    TRIGGER: "#8B5CF6",
};

export default function AuditLog() {
    const [logs, setLogs] = useState<AuditLogItem[]>([]);
    const [entityTypes, setEntityTypes] = useState<string[]>([]);
    const [filter, setFilter] = useState("");
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    async function load() {
        try {
            setLoading(true);
            const [l, et] = await Promise.all([listAuditLogs(filter || undefined), listEntityTypes()]);
            setLogs(l);
            setEntityTypes(et);
        } catch {
            setError("Erro ao carregar log de auditoria.");
        } finally {
            setLoading(false);
        }
    }

    useEffect(() => { load(); }, [filter]);

    return (
        <Box>
            <Typography variant="h5" fontWeight="bold" color="#F8FAFC" gutterBottom>
                Log de Auditoria
            </Typography>
            <Typography variant="body2" color="#94A3B8" sx={{ mb: 3 }}>
                Histórico de todas as ações realizadas na plataforma
            </Typography>

            {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}

            <TextField
                select
                label="Filtrar por entidade"
                value={filter}
                onChange={(e) => setFilter(e.target.value)}
                sx={{ mb: 2, minWidth: 240 }}
                InputLabelProps={{ sx: { color: "#94A3B8" } }}
                InputProps={{ sx: { color: "#F8FAFC" } }}
            >
                <MenuItem value="">Todas</MenuItem>
                {entityTypes.map((t) => <MenuItem key={t} value={t}>{t}</MenuItem>)}
            </TextField>

            {loading ? (
                <Box sx={{ display: "flex", justifyContent: "center", pt: 6 }}><CircularProgress sx={{ color: "#F97316" }} /></Box>
            ) : (
                <TableContainer component={Paper} sx={{ backgroundColor: "#0F172A", border: "1px solid #334155" }}>
                    <Table size="small">
                        <TableHead>
                            <TableRow>
                                <TableCell sx={{ color: "#64748B" }}>Data</TableCell>
                                <TableCell sx={{ color: "#64748B" }}>Entidade</TableCell>
                                <TableCell sx={{ color: "#64748B" }}>Ação</TableCell>
                                <TableCell sx={{ color: "#64748B" }}>Descrição</TableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {logs.map((log) => (
                                <TableRow key={log.id}>
                                    <TableCell sx={{ color: "#94A3B8", whiteSpace: "nowrap" }}>
                                        {log.created_at ? new Date(log.created_at).toLocaleString("pt-BR") : ""}
                                    </TableCell>
                                    <TableCell sx={{ color: "#F8FAFC" }}>{log.entity_type}</TableCell>
                                    <TableCell>
                                        <Chip label={log.action} size="small" sx={{ height: 20, fontSize: 10, backgroundColor: `${actionColors[log.action] || "#64748B"}22`, color: actionColors[log.action] || "#64748B" }} />
                                    </TableCell>
                                    <TableCell sx={{ color: "#CBD5E1" }}>{log.description}</TableCell>
                                </TableRow>
                            ))}
                            {logs.length === 0 && (
                                <TableRow><TableCell colSpan={4} sx={{ color: "#94A3B8", textAlign: "center" }}>Nenhum registro encontrado.</TableCell></TableRow>
                            )}
                        </TableBody>
                    </Table>
                </TableContainer>
            )}
        </Box>
    );
}
