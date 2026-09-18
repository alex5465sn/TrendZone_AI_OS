import { useEffect, useState } from "react";

import {
    Box,
    Typography,
    Card,
    CardContent,
    Chip,
    Button,
    CircularProgress,
    Alert,
    Grid,
    Dialog,
    DialogTitle,
    DialogContent,
    DialogActions,
    TextField,
    MenuItem,
    Snackbar,
    IconButton,
} from "@mui/material";

import AddIcon from "@mui/icons-material/Add";
import CheckCircleIcon from "@mui/icons-material/CheckCircle";
import DeleteIcon from "@mui/icons-material/Delete";
import WarningAmberIcon from "@mui/icons-material/WarningAmber";
import ScheduleIcon from "@mui/icons-material/Schedule";

import {
    listFollowUps,
    getOverdueFollowUps,
    createFollowUp,
    updateFollowUpStatus,
    deleteFollowUp,
    type FollowUpItem,
} from "../../services/followUpService";

const priorityColors: Record<string, string> = { HIGH: "#EF4444", MEDIUM: "#F59E0B", LOW: "#10B981" };

export default function FollowUps() {
    const [items, setItems] = useState<FollowUpItem[]>([]);
    const [overdue, setOverdue] = useState<FollowUpItem[]>([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");
    const [toast, setToast] = useState("");
    const [dialogOpen, setDialogOpen] = useState(false);
    const [form, setForm] = useState({ message: "", due_at: "", priority: "MEDIUM" });

    async function load() {
        try {
            setLoading(true);
            const [all, od] = await Promise.all([listFollowUps(), getOverdueFollowUps()]);
            setItems(all);
            setOverdue(od);
        } catch {
            setError("Erro ao carregar follow-ups.");
        } finally {
            setLoading(false);
        }
    }

    useEffect(() => { load(); }, []);

    async function handleCreate() {
        if (!form.message.trim()) return;
        try {
            await createFollowUp(form);
            setDialogOpen(false);
            setToast("Follow-up criado!");
            setForm({ message: "", due_at: "", priority: "MEDIUM" });
            load();
        } catch {
            setError("Erro ao criar.");
        }
    }

    async function handleComplete(id: number) {
        await updateFollowUpStatus(id, "DONE");
        setToast("Concluído!");
        load();
    }

    async function handleDelete(id: number) {
        await deleteFollowUp(id);
        setToast("Removido.");
        load();
    }

    return (
        <Box>
            <Box sx={{ display: "flex", justifyContent: "space-between", mb: 3 }}>
                <Box>
                    <Typography variant="h5" fontWeight="bold" color="#F8FAFC">
                        Follow-ups & Radar
                    </Typography>
                    <Typography variant="body2" color="#94A3B8">
                        Nunca perca uma oportunidade — acompanhe cada ação pendente
                    </Typography>
                </Box>
                <Button variant="contained" startIcon={<AddIcon />} onClick={() => setDialogOpen(true)} sx={{ backgroundColor: "#2563EB" }}>
                    Novo Follow-up
                </Button>
            </Box>

            {error && <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError("")}>{error}</Alert>}

            {overdue.length > 0 && (
                <Alert severity="warning" icon={<WarningAmberIcon />} sx={{ mb: 3, backgroundColor: "#F59E0B22", color: "#F59E0B", border: "1px solid #F59E0B44" }}>
                    {overdue.length} follow-up(s) atrasado(s)! Ação necessária.
                </Alert>
            )}

            {loading ? (
                <Box sx={{ display: "flex", justifyContent: "center", pt: 6 }}><CircularProgress sx={{ color: "#F97316" }} /></Box>
            ) : items.length === 0 ? (
                <Typography color="#94A3B8">Nenhum follow-up registrado.</Typography>
            ) : (
                <Grid container spacing={2}>
                    {items.map((item) => {
                        const isOverdue = overdue.some((o) => o.id === item.id);
                        return (
                            <Grid item xs={12} sm={6} md={4} key={item.id}>
                                <Card sx={{
                                    backgroundColor: "#0F172A",
                                    border: `1px solid ${isOverdue ? "#EF4444" : "#334155"}`,
                                    height: "100%",
                                }}>
                                    <CardContent>
                                        <Box sx={{ display: "flex", justifyContent: "space-between", mb: 1 }}>
                                            <Chip
                                                label={item.priority}
                                                size="small"
                                                sx={{ height: 20, fontSize: 10, backgroundColor: `${priorityColors[item.priority]}22`, color: priorityColors[item.priority] }}
                                            />
                                            <Chip
                                                label={item.status}
                                                size="small"
                                                sx={{ height: 20, fontSize: 10, backgroundColor: item.status === "DONE" ? "#10B98122" : "#1E293B", color: item.status === "DONE" ? "#10B981" : "#94A3B8" }}
                                            />
                                        </Box>
                                        <Typography variant="body2" color="#F8FAFC" sx={{ mb: 1 }}>
                                            {item.message}
                                        </Typography>
                                        {item.due_at && (
                                            <Box sx={{ display: "flex", alignItems: "center", gap: 0.5, mb: 1 }}>
                                                <ScheduleIcon sx={{ fontSize: 14, color: isOverdue ? "#EF4444" : "#64748B" }} />
                                                <Typography variant="caption" color={isOverdue ? "#EF4444" : "#64748B"}>
                                                    {new Date(item.due_at).toLocaleDateString("pt-BR")}
                                                    {item.days_overdue ? ` (${item.days_overdue}d atrasado)` : ""}
                                                </Typography>
                                            </Box>
                                        )}
                                        <Box sx={{ display: "flex", gap: 0.5, mt: 1 }}>
                                            {item.status !== "DONE" && (
                                                <IconButton size="small" onClick={() => handleComplete(item.id)} sx={{ color: "#10B981" }}>
                                                    <CheckCircleIcon fontSize="small" />
                                                </IconButton>
                                            )}
                                            <IconButton size="small" onClick={() => handleDelete(item.id)} sx={{ color: "#EF4444" }}>
                                                <DeleteIcon fontSize="small" />
                                            </IconButton>
                                        </Box>
                                    </CardContent>
                                </Card>
                            </Grid>
                        );
                    })}
                </Grid>
            )}

            <Dialog open={dialogOpen} onClose={() => setDialogOpen(false)} maxWidth="sm" fullWidth PaperProps={{ sx: { backgroundColor: "#0F172A", color: "#F8FAFC" } }}>
                <DialogTitle>Novo Follow-up</DialogTitle>
                <DialogContent sx={{ display: "flex", flexDirection: "column", gap: 2, pt: "8px !important" }}>
                    <TextField label="Mensagem" value={form.message} onChange={(e) => setForm({ ...form, message: e.target.value })} multiline rows={3} fullWidth InputLabelProps={{ sx: { color: "#94A3B8" } }} InputProps={{ sx: { color: "#F8FAFC" } }} />
                    <TextField label="Data limite" type="datetime-local" value={form.due_at} onChange={(e) => setForm({ ...form, due_at: e.target.value })} InputLabelProps={{ shrink: true, sx: { color: "#94A3B8" } }} InputProps={{ sx: { color: "#F8FAFC" } }} />
                    <TextField select label="Prioridade" value={form.priority} onChange={(e) => setForm({ ...form, priority: e.target.value })} InputLabelProps={{ sx: { color: "#94A3B8" } }} InputProps={{ sx: { color: "#F8FAFC" } }}>
                        <MenuItem value="HIGH">Alta</MenuItem>
                        <MenuItem value="MEDIUM">Média</MenuItem>
                        <MenuItem value="LOW">Baixa</MenuItem>
                    </TextField>
                </DialogContent>
                <DialogActions>
                    <Button onClick={() => setDialogOpen(false)} sx={{ color: "#94A3B8" }}>Cancelar</Button>
                    <Button onClick={handleCreate} variant="contained" sx={{ backgroundColor: "#2563EB" }}>Criar</Button>
                </DialogActions>
            </Dialog>

            <Snackbar open={!!toast} autoHideDuration={3000} onClose={() => setToast("")} message={toast} />
        </Box>
    );
}
