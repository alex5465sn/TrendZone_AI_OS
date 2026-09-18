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
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow,
    Paper,
    LinearProgress,
    MenuItem,
} from "@mui/material";

import AddIcon from "@mui/icons-material/Add";
import DeleteIcon from "@mui/icons-material/Delete";

import {
    getChannels,
    listTrackings,
    getChannelSummary,
    createTracking,
    deleteTracking,
    type ChannelTrackingItem,
    type ChannelSummary,
} from "../../services/channelTrackingService";

const channelColors: Record<string, string> = {
    shopee_video: "#EE4D2D",
    pinterest: "#E60023",
    whatsapp: "#25D366",
    facebook: "#1877F2",
    instagram: "#E4405F",
    tiktok: "#000000",
    blog: "#F97316",
    telegram: "#0088CC",
};

export default function Channels() {
    const [channels, setChannels] = useState<{ id: string; name: string }[]>([]);
    const [summary, setSummary] = useState<ChannelSummary[]>([]);
    const [trackings, setTrackings] = useState<ChannelTrackingItem[]>([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");
    const [toast, setToast] = useState("");
    const [dialogOpen, setDialogOpen] = useState(false);
    const [form, setForm] = useState({ channel: "", sub_id: "", tracking_url: "" });

    async function load() {
        try {
            setLoading(true);
            const [ch, sm, tr] = await Promise.all([getChannels(), getChannelSummary(), listTrackings()]);
            setChannels(ch);
            setSummary(sm);
            setTrackings(tr);
        } catch {
            setError("Erro ao carregar dados.");
        } finally {
            setLoading(false);
        }
    }

    useEffect(() => { load(); }, []);

    async function handleCreate() {
        if (!form.channel || !form.sub_id) return;
        try {
            await createTracking(form);
            setDialogOpen(false);
            setForm({ channel: "", sub_id: "", tracking_url: "" });
            setToast("Tracking criado!");
            load();
        } catch {
            setError("Erro ao criar tracking.");
        }
    }

    async function handleDelete(id: number) {
        await deleteTracking(id);
        setToast("Removido.");
        load();
    }

    const maxRevenue = Math.max(...summary.map((s) => s.total_revenue), 1);

    return (
        <Box>
            <Box sx={{ display: "flex", justifyContent: "space-between", mb: 3 }}>
                <Box>
                    <Typography variant="h5" fontWeight="bold" color="#F8FAFC">
                        Canais & SubID Tracking
                    </Typography>
                    <Typography variant="body2" color="#94A3B8">
                        Rastreie performance por canal com SubIDs únicos
                    </Typography>
                </Box>
                <Button variant="contained" startIcon={<AddIcon />} onClick={() => setDialogOpen(true)} sx={{ backgroundColor: "#2563EB" }}>
                    Novo Tracking
                </Button>
            </Box>

            {error && <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError("")}>{error}</Alert>}

            {loading ? (
                <Box sx={{ display: "flex", justifyContent: "center", pt: 6 }}><CircularProgress sx={{ color: "#F97316" }} /></Box>
            ) : (
                <>
                    <Typography variant="h6" color="#F8FAFC" sx={{ mb: 2 }}>Resumo por Canal</Typography>
                    <Grid container spacing={2} sx={{ mb: 4 }}>
                        {summary.map((s) => (
                            <Grid item xs={12} sm={6} md={4} lg={3} key={s.channel}>
                                <Card sx={{ backgroundColor: "#0F172A", border: `1px solid ${channelColors[s.channel] || "#334155"}` }}>
                                    <CardContent>
                                        <Chip label={s.channel} size="small" sx={{ backgroundColor: channelColors[s.channel] || "#64748B", color: "#fff", mb: 1 }} />
                                        <Box sx={{ mb: 1 }}>
                                            <Typography variant="caption" color="#64748B">Receita Total</Typography>
                                            <Typography variant="h6" color="#10B981" fontWeight="bold">R$ {s.total_revenue.toFixed(2)}</Typography>
                                            <LinearProgress
                                                variant="determinate"
                                                value={(s.total_revenue / maxRevenue) * 100}
                                                sx={{ height: 4, borderRadius: 2, mt: 0.5, backgroundColor: "#1E293B", "& .MuiLinearProgress-bar": { backgroundColor: channelColors[s.channel] || "#3B82F6" } }}
                                            />
                                        </Box>
                                        <Box sx={{ display: "flex", gap: 2, mt: 1 }}>
                                            <Box>
                                                <Typography variant="caption" color="#64748B">Cliques</Typography>
                                                <Typography variant="body2" color="#F8FAFC" fontWeight={600}>{s.total_clicks}</Typography>
                                            </Box>
                                            <Box>
                                                <Typography variant="caption" color="#64748B">Conversões</Typography>
                                                <Typography variant="body2" color="#F8FAFC" fontWeight={600}>{s.total_conversions}</Typography>
                                            </Box>
                                            <Box>
                                                <Typography variant="caption" color="#64748B">CTR</Typography>
                                                <Typography variant="body2" color="#F59E0B" fontWeight={600}>{s.avg_ctr}%</Typography>
                                            </Box>
                                        </Box>
                                    </CardContent>
                                </Card>
                            </Grid>
                        ))}
                        {summary.length === 0 && <Grid item xs={12}><Typography color="#94A3B8">Nenhum dado de canal registrado.</Typography></Grid>}
                    </Grid>

                    <Typography variant="h6" color="#F8FAFC" sx={{ mb: 2 }}>Links de Rastreamento</Typography>
                    <TableContainer component={Paper} sx={{ backgroundColor: "#0F172A", border: "1px solid #334155" }}>
                        <Table size="small">
                            <TableHead>
                                <TableRow>
                                    <TableCell sx={{ color: "#64748B" }}>Canal</TableCell>
                                    <TableCell sx={{ color: "#64748B" }}>SubID</TableCell>
                                    <TableCell sx={{ color: "#64748B" }}>Cliques</TableCell>
                                    <TableCell sx={{ color: "#64748B" }}>Conv.</TableCell>
                                    <TableCell sx={{ color: "#64748B" }}>Receita</TableCell>
                                    <TableCell sx={{ color: "#64748B" }}>CTR</TableCell>
                                    <TableCell sx={{ color: "#64748B" }}></TableCell>
                                </TableRow>
                            </TableHead>
                            <TableBody>
                                {trackings.map((t) => (
                                    <TableRow key={t.id}>
                                        <TableCell>
                                            <Chip label={t.channel} size="small" sx={{ backgroundColor: channelColors[t.channel] || "#64748B", color: "#fff", height: 22, fontSize: 11 }} />
                                        </TableCell>
                                        <TableCell sx={{ color: "#F8FAFC" }}>{t.sub_id}</TableCell>
                                        <TableCell sx={{ color: "#F8FAFC" }}>{t.clicks}</TableCell>
                                        <TableCell sx={{ color: "#F8FAFC" }}>{t.conversions}</TableCell>
                                        <TableCell sx={{ color: "#10B981" }}>R$ {t.revenue.toFixed(2)}</TableCell>
                                        <TableCell sx={{ color: "#F59E0B" }}>{t.ctr}%</TableCell>
                                        <TableCell>
                                            <IconButton size="small" onClick={() => handleDelete(t.id)} sx={{ color: "#EF4444" }}><DeleteIcon fontSize="small" /></IconButton>
                                        </TableCell>
                                    </TableRow>
                                ))}
                                {trackings.length === 0 && (
                                    <TableRow><TableCell colSpan={7} sx={{ color: "#94A3B8", textAlign: "center" }}>Nenhum tracking criado.</TableCell></TableRow>
                                )}
                            </TableBody>
                        </Table>
                    </TableContainer>
                </>
            )}

            <Dialog open={dialogOpen} onClose={() => setDialogOpen(false)} maxWidth="sm" fullWidth PaperProps={{ sx: { backgroundColor: "#0F172A", color: "#F8FAFC" } }}>
                <DialogTitle>Novo Tracking de Canal</DialogTitle>
                <DialogContent sx={{ display: "flex", flexDirection: "column", gap: 2, pt: "8px !important" }}>
                    <TextField select label="Canal" value={form.channel} onChange={(e) => setForm({ ...form, channel: e.target.value })} fullWidth InputLabelProps={{ sx: { color: "#94A3B8" } }} InputProps={{ sx: { color: "#F8FAFC" } }}>
                        {channels.map((c) => <MenuItem key={c.id} value={c.id}>{c.name}</MenuItem>)}
                    </TextField>
                    <TextField label="SubID" value={form.sub_id} onChange={(e) => setForm({ ...form, sub_id: e.target.value })} placeholder="Ex: Pin_12345, WA_grupo1" fullWidth InputLabelProps={{ sx: { color: "#94A3B8" } }} InputProps={{ sx: { color: "#F8FAFC" } }} />
                    <TextField label="URL de Rastreamento" value={form.tracking_url} onChange={(e) => setForm({ ...form, tracking_url: e.target.value })} fullWidth InputLabelProps={{ sx: { color: "#94A3B8" } }} InputProps={{ sx: { color: "#F8FAFC" } }} />
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
