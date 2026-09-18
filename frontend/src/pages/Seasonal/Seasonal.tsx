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
    Snackbar,
    IconButton,
    LinearProgress,
} from "@mui/material";

import EventIcon from "@mui/icons-material/Event";
import AutoFixHighIcon from "@mui/icons-material/AutoFixHigh";
import DeleteIcon from "@mui/icons-material/Delete";
import PlayArrowIcon from "@mui/icons-material/PlayArrow";

import {
    listEvents,
    seedEvents,
    createEvent,
    updateEvent,
    deleteEvent,
    type SeasonalEventItem,
} from "../../services/seasonalService";

const categoryColors: Record<string, string> = {
    comemorativa: "#8B5CF6",
    sazonal: "#F59E0B",
    marketplace: "#EE4D2D",
};

export default function Seasonal() {
    const [events, setEvents] = useState<SeasonalEventItem[]>([]);
    const [loading, setLoading] = useState(false);
    const [seeding, setSeeding] = useState(false);
    const [error, setError] = useState("");
    const [toast, setToast] = useState("");
    const [dialogOpen, setDialogOpen] = useState(false);
    const [form, setForm] = useState({ name: "", event_date: "", category: "", niches: "", strategy_notes: "" });

    async function load() {
        try {
            setLoading(true);
            setEvents(await listEvents());
        } catch {
            setError("Erro ao carregar eventos.");
        } finally {
            setLoading(false);
        }
    }

    useEffect(() => { load(); }, []);

    async function handleSeed() {
        try {
            setSeeding(true);
            const result = await seedEvents();
            setToast(`${(result as any).created || 0} eventos criados!`);
            load();
        } catch {
            setError("Erro ao semear eventos.");
        } finally {
            setSeeding(false);
        }
    }

    async function handleCreate() {
        if (!form.name || !form.event_date) return;
        try {
            await createEvent(form);
            setDialogOpen(false);
            setForm({ name: "", event_date: "", category: "", niches: "", strategy_notes: "" });
            setToast("Evento criado!");
            load();
        } catch {
            setError("Erro ao criar evento.");
        }
    }

    async function handleDelete(id: number) {
        await deleteEvent(id);
        setToast("Removido.");
        load();
    }

    async function handleActivate(id: number) {
        await updateEvent(id, { status: "ACTIVE" });
        setToast("Evento ativado!");
        load();
    }

    function urgencyLevel(days: number | null) {
        if (days === null) return "#64748B";
        if (days <= 7) return "#EF4444";
        if (days <= 30) return "#F59E0B";
        if (days <= 60) return "#3B82F6";
        return "#10B981";
    }

    return (
        <Box>
            <Box sx={{ display: "flex", justifyContent: "space-between", mb: 3, flexWrap: "wrap", gap: 1 }}>
                <Box>
                    <Typography variant="h5" fontWeight="bold" color="#F8FAFC">
                        Calendário Sazonal
                    </Typography>
                    <Typography variant="body2" color="#94A3B8">
                        Planeje campanhas com antecedência para datas estratégicas
                    </Typography>
                </Box>
                <Box sx={{ display: "flex", gap: 1 }}>
                    <Button
                        variant="outlined"
                        startIcon={<AutoFixHighIcon />}
                        onClick={handleSeed}
                        disabled={seeding}
                        sx={{ borderColor: "#F97316", color: "#F97316" }}
                    >
                        {seeding ? "Carregando..." : "Carregar Datas Padrão"}
                    </Button>
                    <Button variant="contained" startIcon={<EventIcon />} onClick={() => setDialogOpen(true)} sx={{ backgroundColor: "#2563EB" }}>
                        Novo Evento
                    </Button>
                </Box>
            </Box>

            {error && <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError("")}>{error}</Alert>}

            {loading ? (
                <Box sx={{ display: "flex", justifyContent: "center", pt: 6 }}><CircularProgress sx={{ color: "#F97316" }} /></Box>
            ) : events.length === 0 ? (
                <Box sx={{ textAlign: "center", pt: 6 }}>
                    <Typography color="#94A3B8" sx={{ mb: 2 }}>Nenhum evento sazonal cadastrado.</Typography>
                    <Button variant="contained" onClick={handleSeed} sx={{ backgroundColor: "#F97316" }}>
                        Carregar Calendário Padrão (Datas BR + Shopee)
                    </Button>
                </Box>
            ) : (
                <Grid container spacing={2}>
                    {events.map((evt) => (
                        <Grid item xs={12} sm={6} md={4} lg={3} key={evt.id}>
                            <Card sx={{
                                backgroundColor: "#0F172A",
                                border: `1px solid ${evt.is_prep_phase ? "#F59E0B" : "#334155"}`,
                                height: "100%",
                                position: "relative",
                                overflow: "visible",
                            }}>
                                {evt.is_prep_phase && (
                                    <Chip
                                        label="EM PREPARAÇÃO"
                                        size="small"
                                        sx={{
                                            position: "absolute",
                                            top: -10,
                                            right: 8,
                                            height: 20,
                                            fontSize: 10,
                                            backgroundColor: "#F59E0B",
                                            color: "#000",
                                            fontWeight: 700,
                                        }}
                                    />
                                )}
                                <CardContent>
                                    <Box sx={{ display: "flex", justifyContent: "space-between", mb: 1 }}>
                                        <Chip
                                            label={evt.category || "geral"}
                                            size="small"
                                            sx={{ height: 20, fontSize: 10, backgroundColor: `${categoryColors[evt.category] || "#64748B"}33`, color: categoryColors[evt.category] || "#64748B" }}
                                        />
                                        <Chip
                                            label={evt.status}
                                            size="small"
                                            sx={{ height: 20, fontSize: 10, backgroundColor: "#1E293B", color: "#94A3B8" }}
                                        />
                                    </Box>

                                    <Typography variant="subtitle1" color="#F8FAFC" fontWeight="bold" sx={{ mb: 0.5 }}>
                                        {evt.name}
                                    </Typography>

                                    <Typography variant="body2" color="#94A3B8" sx={{ mb: 1 }}>
                                        {evt.event_date ? new Date(evt.event_date).toLocaleDateString("pt-BR", { day: "2-digit", month: "long", year: "numeric" }) : ""}
                                    </Typography>

                                    {evt.days_until !== null && (
                                        <Box sx={{ mb: 1 }}>
                                            <Box sx={{ display: "flex", justifyContent: "space-between" }}>
                                                <Typography variant="caption" color="#64748B">Faltam</Typography>
                                                <Typography variant="caption" color={urgencyLevel(evt.days_until)} fontWeight={700}>
                                                    {evt.days_until} dias
                                                </Typography>
                                            </Box>
                                            <LinearProgress
                                                variant="determinate"
                                                value={Math.max(0, Math.min(100, 100 - (evt.days_until / 365) * 100))}
                                                sx={{
                                                    height: 4,
                                                    borderRadius: 2,
                                                    mt: 0.5,
                                                    backgroundColor: "#1E293B",
                                                    "& .MuiLinearProgress-bar": { backgroundColor: urgencyLevel(evt.days_until) },
                                                }}
                                            />
                                        </Box>
                                    )}

                                    {evt.niches && (
                                        <Box sx={{ mb: 1 }}>
                                            <Typography variant="caption" color="#64748B">Nichos:</Typography>
                                            <Typography variant="caption" color="#CBD5E1" sx={{ display: "block" }}>
                                                {evt.niches}
                                            </Typography>
                                        </Box>
                                    )}

                                    <Box sx={{ display: "flex", gap: 0.5, mt: 1 }}>
                                        <IconButton size="small" onClick={() => handleActivate(evt.id)} sx={{ color: "#10B981" }}>
                                            <PlayArrowIcon fontSize="small" />
                                        </IconButton>
                                        <IconButton size="small" onClick={() => handleDelete(evt.id)} sx={{ color: "#EF4444" }}>
                                            <DeleteIcon fontSize="small" />
                                        </IconButton>
                                    </Box>
                                </CardContent>
                            </Card>
                        </Grid>
                    ))}
                </Grid>
            )}

            <Dialog open={dialogOpen} onClose={() => setDialogOpen(false)} maxWidth="sm" fullWidth PaperProps={{ sx: { backgroundColor: "#0F172A", color: "#F8FAFC" } }}>
                <DialogTitle>Novo Evento Sazonal</DialogTitle>
                <DialogContent sx={{ display: "flex", flexDirection: "column", gap: 2, pt: "8px !important" }}>
                    <TextField label="Nome do evento" value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} fullWidth InputLabelProps={{ sx: { color: "#94A3B8" } }} InputProps={{ sx: { color: "#F8FAFC" } }} />
                    <TextField label="Data" type="date" value={form.event_date} onChange={(e) => setForm({ ...form, event_date: e.target.value })} InputLabelProps={{ shrink: true, sx: { color: "#94A3B8" } }} InputProps={{ sx: { color: "#F8FAFC" } }} />
                    <TextField label="Categoria" value={form.category} onChange={(e) => setForm({ ...form, category: e.target.value })} placeholder="comemorativa, sazonal, marketplace" InputLabelProps={{ sx: { color: "#94A3B8" } }} InputProps={{ sx: { color: "#F8FAFC" } }} />
                    <TextField label="Nichos relevantes" value={form.niches} onChange={(e) => setForm({ ...form, niches: e.target.value })} multiline rows={2} InputLabelProps={{ sx: { color: "#94A3B8" } }} InputProps={{ sx: { color: "#F8FAFC" } }} />
                    <TextField label="Notas de estratégia" value={form.strategy_notes} onChange={(e) => setForm({ ...form, strategy_notes: e.target.value })} multiline rows={2} InputLabelProps={{ sx: { color: "#94A3B8" } }} InputProps={{ sx: { color: "#F8FAFC" } }} />
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
