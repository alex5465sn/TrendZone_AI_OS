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
    IconButton,
    Dialog,
    DialogTitle,
    DialogContent,
    DialogActions,
    TextField,
    MenuItem,
    Snackbar,
    Badge,
} from "@mui/material";

import AddIcon from "@mui/icons-material/Add";
import DeleteIcon from "@mui/icons-material/Delete";
import DragIndicatorIcon from "@mui/icons-material/DragIndicator";
import WarningIcon from "@mui/icons-material/Warning";

import AutoAwesomeIcon from "@mui/icons-material/AutoAwesome";

import {
    getStages,
    createCard,
    moveCard,
    deleteCard,
    getRadar,
    autoPopulate,
    type FunnelStage,
    type CardCreate,
} from "../../services/funnelService";

const priorityColors: Record<string, string> = {
    HIGH: "#EF4444",
    MEDIUM: "#F59E0B",
    LOW: "#10B981",
};

export default function Funnel() {
    const [stages, setStages] = useState<FunnelStage[]>([]);
    const [radar, setRadar] = useState<any[]>([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");
    const [toast, setToast] = useState("");
    const [dialogOpen, setDialogOpen] = useState(false);
    const [dragCard, setDragCard] = useState<{ cardId: number; fromStage: number } | null>(null);
    const [form, setForm] = useState<CardCreate>({
        stage_id: 0,
        title: "",
        description: "",
        priority: "MEDIUM",
        estimated_revenue: 0,
        channel: "",
        notes: "",
    });

    async function load() {
        try {
            setLoading(true);
            const [s, r] = await Promise.all([getStages(), getRadar()]);
            setStages(s);
            setRadar(r);
        } catch {
            setError("Erro ao carregar funil.");
        } finally {
            setLoading(false);
        }
    }

    useEffect(() => { load(); }, []);

    const [syncing, setSyncing] = useState(false);

    async function handleAutoPopulate() {
        try {
            setSyncing(true);
            const result = await autoPopulate();
            setToast(`${result.created} card(s) criado(s) automaticamente pela IA.`);
            await load();
        } catch {
            setError("Erro ao sincronizar com a IA.");
        } finally {
            setSyncing(false);
        }
    }

    function openNewCard(stageId: number) {
        setForm({ ...form, stage_id: stageId, title: "", description: "", notes: "" });
        setDialogOpen(true);
    }

    async function handleCreateCard() {
        if (!form.title.trim()) return;
        try {
            await createCard(form);
            setDialogOpen(false);
            setToast("Card criado!");
            load();
        } catch {
            setError("Erro ao criar card.");
        }
    }

    async function handleDelete(cardId: number) {
        try {
            await deleteCard(cardId);
            setToast("Card removido.");
            load();
        } catch {
            setError("Erro ao remover card.");
        }
    }

    function handleDragStart(cardId: number, fromStage: number) {
        setDragCard({ cardId, fromStage });
    }

    async function handleDrop(toStageId: number) {
        if (!dragCard || dragCard.fromStage === toStageId) {
            setDragCard(null);
            return;
        }
        try {
            await moveCard(dragCard.cardId, toStageId, 0);
            setToast("Card movido!");
            load();
        } catch {
            setError("Erro ao mover card.");
        }
        setDragCard(null);
    }

    if (loading && stages.length === 0) {
        return (
            <Box sx={{ display: "flex", justifyContent: "center", pt: 10 }}>
                <CircularProgress sx={{ color: "#F97316" }} />
            </Box>
        );
    }

    return (
        <Box>
            <Box sx={{ display: "flex", justifyContent: "space-between", mb: 3 }}>
                <Box>
                    <Typography variant="h5" fontWeight="bold" color="#F8FAFC">
                        Funil de Vendas
                    </Typography>
                    <Typography variant="body2" color="#94A3B8">
                        Kanban para gerenciar o ciclo de vida dos seus produtos
                    </Typography>
                </Box>
                <Button
                    variant="contained"
                    startIcon={<AutoAwesomeIcon />}
                    onClick={handleAutoPopulate}
                    disabled={syncing}
                    sx={{ backgroundColor: "#F97316", "&:hover": { backgroundColor: "#EA580C" }, height: "fit-content" }}
                >
                    {syncing ? "Sincronizando..." : "Sincronizar com IA"}
                </Button>
                {radar.length > 0 && (
                    <Badge badgeContent={radar.length} color="error">
                        <Chip
                            icon={<WarningIcon />}
                            label={`${radar.length} oportunidade(s) parada(s)`}
                            sx={{ backgroundColor: "#1E293B", color: "#F59E0B" }}
                        />
                    </Badge>
                )}
            </Box>

            {error && <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError("")}>{error}</Alert>}

            <Box
                sx={{
                    display: "flex",
                    gap: 2,
                    overflowX: "auto",
                    pb: 2,
                    minHeight: "70vh",
                }}
            >
                {stages.map((stage) => (
                    <Box
                        key={stage.id}
                        onDragOver={(e) => e.preventDefault()}
                        onDrop={() => handleDrop(stage.id)}
                        sx={{
                            minWidth: 280,
                            maxWidth: 320,
                            flex: "0 0 auto",
                            backgroundColor: "#0F172A",
                            borderRadius: 2,
                            border: `2px solid ${stage.color}33`,
                            display: "flex",
                            flexDirection: "column",
                        }}
                    >
                        <Box
                            sx={{
                                p: 2,
                                borderBottom: `2px solid ${stage.color}`,
                                display: "flex",
                                justifyContent: "space-between",
                                alignItems: "center",
                            }}
                        >
                            <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
                                <Box sx={{ width: 10, height: 10, borderRadius: "50%", backgroundColor: stage.color }} />
                                <Typography variant="subtitle2" color="#F8FAFC" fontWeight="bold">
                                    {stage.name}
                                </Typography>
                                <Chip
                                    label={stage.cards.length}
                                    size="small"
                                    sx={{ backgroundColor: "#1E293B", color: "#94A3B8", height: 20, fontSize: 11 }}
                                />
                            </Box>
                            <IconButton size="small" onClick={() => openNewCard(stage.id)} sx={{ color: "#94A3B8" }}>
                                <AddIcon fontSize="small" />
                            </IconButton>
                        </Box>

                        <Box sx={{ p: 1, flex: 1, overflowY: "auto" }}>
                            {stage.cards.map((card) => (
                                <Card
                                    key={card.id}
                                    draggable
                                    onDragStart={() => handleDragStart(card.id, stage.id)}
                                    sx={{
                                        mb: 1,
                                        backgroundColor: "#1E293B",
                                        cursor: "grab",
                                        "&:hover": { backgroundColor: "#263548" },
                                        border: "1px solid #334155",
                                    }}
                                >
                                    <CardContent sx={{ p: "12px !important" }}>
                                        <Box sx={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start" }}>
                                            <Box sx={{ display: "flex", gap: 0.5, alignItems: "center" }}>
                                                <DragIndicatorIcon sx={{ fontSize: 14, color: "#475569" }} />
                                                <Typography variant="body2" color="#F8FAFC" fontWeight={600} sx={{ fontSize: 13 }}>
                                                    {card.title}
                                                </Typography>
                                            </Box>
                                            <IconButton size="small" onClick={() => handleDelete(card.id)} sx={{ color: "#475569", p: 0 }}>
                                                <DeleteIcon sx={{ fontSize: 14 }} />
                                            </IconButton>
                                        </Box>
                                        {card.description && (
                                            <Typography variant="caption" color="#94A3B8" sx={{ mt: 0.5, display: "block" }}>
                                                {card.description.slice(0, 80)}
                                            </Typography>
                                        )}
                                        <Box sx={{ display: "flex", gap: 0.5, mt: 1, flexWrap: "wrap" }}>
                                            <Chip
                                                label={card.priority}
                                                size="small"
                                                sx={{
                                                    height: 18,
                                                    fontSize: 10,
                                                    backgroundColor: `${priorityColors[card.priority] || "#64748B"}22`,
                                                    color: priorityColors[card.priority] || "#64748B",
                                                }}
                                            />
                                            {card.estimated_revenue > 0 && (
                                                <Chip
                                                    label={`R$ ${card.estimated_revenue.toFixed(2)}`}
                                                    size="small"
                                                    sx={{ height: 18, fontSize: 10, backgroundColor: "#10B98122", color: "#10B981" }}
                                                />
                                            )}
                                            {card.channel && (
                                                <Chip
                                                    label={card.channel}
                                                    size="small"
                                                    sx={{ height: 18, fontSize: 10, backgroundColor: "#3B82F622", color: "#3B82F6" }}
                                                />
                                            )}
                                        </Box>
                                    </CardContent>
                                </Card>
                            ))}
                        </Box>
                    </Box>
                ))}
            </Box>

            <Dialog open={dialogOpen} onClose={() => setDialogOpen(false)} maxWidth="sm" fullWidth PaperProps={{ sx: { backgroundColor: "#0F172A", color: "#F8FAFC" } }}>
                <DialogTitle>Novo Card</DialogTitle>
                <DialogContent sx={{ display: "flex", flexDirection: "column", gap: 2, pt: "8px !important" }}>
                    <TextField label="Título" value={form.title} onChange={(e) => setForm({ ...form, title: e.target.value })} fullWidth InputLabelProps={{ sx: { color: "#94A3B8" } }} InputProps={{ sx: { color: "#F8FAFC" } }} />
                    <TextField label="Descrição" value={form.description} onChange={(e) => setForm({ ...form, description: e.target.value })} multiline rows={2} fullWidth InputLabelProps={{ sx: { color: "#94A3B8" } }} InputProps={{ sx: { color: "#F8FAFC" } }} />
                    <TextField select label="Prioridade" value={form.priority} onChange={(e) => setForm({ ...form, priority: e.target.value })} InputLabelProps={{ sx: { color: "#94A3B8" } }} InputProps={{ sx: { color: "#F8FAFC" } }}>
                        <MenuItem value="HIGH">Alta</MenuItem>
                        <MenuItem value="MEDIUM">Média</MenuItem>
                        <MenuItem value="LOW">Baixa</MenuItem>
                    </TextField>
                    <TextField label="Receita Estimada (R$)" type="number" value={form.estimated_revenue} onChange={(e) => setForm({ ...form, estimated_revenue: Number(e.target.value) })} InputLabelProps={{ sx: { color: "#94A3B8" } }} InputProps={{ sx: { color: "#F8FAFC" } }} />
                    <TextField label="Canal" value={form.channel} onChange={(e) => setForm({ ...form, channel: e.target.value })} placeholder="Ex: Pinterest, WhatsApp, Shopee Video" InputLabelProps={{ sx: { color: "#94A3B8" } }} InputProps={{ sx: { color: "#F8FAFC" } }} />
                    <TextField label="Notas" value={form.notes} onChange={(e) => setForm({ ...form, notes: e.target.value })} multiline rows={2} InputLabelProps={{ sx: { color: "#94A3B8" } }} InputProps={{ sx: { color: "#F8FAFC" } }} />
                </DialogContent>
                <DialogActions>
                    <Button onClick={() => setDialogOpen(false)} sx={{ color: "#94A3B8" }}>Cancelar</Button>
                    <Button onClick={handleCreateCard} variant="contained" sx={{ backgroundColor: "#2563EB" }}>Criar</Button>
                </DialogActions>
            </Dialog>

            <Snackbar open={!!toast} autoHideDuration={3000} onClose={() => setToast("")} message={toast} />
        </Box>
    );
}
