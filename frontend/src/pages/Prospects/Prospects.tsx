import { useEffect, useState } from "react";

import {
    Box,
    Typography,
    Grid,
    Card,
    CardContent,
    Chip,
    Button,
    CircularProgress,
    Alert,
    Divider,
    Tabs,
    Tab,
    Snackbar,
    TextField,
    Dialog,
    DialogTitle,
    DialogContent,
    DialogActions,
} from "@mui/material";

import WhatshotIcon from "@mui/icons-material/Whatshot";
import AcUnitIcon from "@mui/icons-material/AcUnit";
import WbSunnyIcon from "@mui/icons-material/WbSunny";
import SearchIcon from "@mui/icons-material/Search";
import ScheduleIcon from "@mui/icons-material/Schedule";
import DeleteIcon from "@mui/icons-material/Delete";
import TravelExploreIcon from "@mui/icons-material/TravelExplore";

import {
    scanProspects,
    listProspects,
    updateProspectStatus,
    deleteProspect,
    createSchedule,
    listSchedules,
    deleteSchedule,
    type Prospect,
    type ScheduleItem,
} from "../../services/prospectService";

function tempIcon(t: string) {
    if (t === "quente") return <WhatshotIcon sx={{ color: "#EF4444" }} />;
    if (t === "morno") return <WbSunnyIcon sx={{ color: "#F59E0B" }} />;
    return <AcUnitIcon sx={{ color: "#38BDF8" }} />;
}

function tempColor(t: string) {
    if (t === "quente") return "#EF4444";
    if (t === "morno") return "#F59E0B";
    return "#38BDF8";
}

export default function Prospects() {

    const [tab, setTab] = useState(0);
    const [prospects, setProspects] = useState<Prospect[]>([]);
    const [schedules, setSchedules] = useState<ScheduleItem[]>([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");
    const [toast, setToast] = useState("");
    const [nichoInput, setNichoInput] = useState("");
    const [scheduleOpen, setScheduleOpen] = useState(false);
    const [schedForm, setSchedForm] = useState({ nicho: "", hora: "09:00", quantos: 5 });

    async function loadProspects() {
        try {
            setLoading(true);
            setError("");
            const data = await listProspects();
            setProspects(data);
        } catch {
            setError("Erro ao carregar prospects.");
        } finally {
            setLoading(false);
        }
    }

    async function loadSchedules() {
        try {
            setLoading(true);
            setError("");
            const data = await listSchedules();
            setSchedules(data);
        } catch {
            setError("Erro ao carregar agendamentos.");
        } finally {
            setLoading(false);
        }
    }

    useEffect(() => {
        if (tab === 0) loadProspects();
        else loadSchedules();
    }, [tab]);

    async function handleScan() {
        try {
            setLoading(true);
            setError("");
            const data = await scanProspects(nichoInput);
            setProspects(data);
            setToast(`${data.length} nicho(s) prospectado(s).`);
        } catch {
            setError("Erro ao prospectar.");
        } finally {
            setLoading(false);
        }
    }

    async function handleContatado(id: number) {
        try {
            await updateProspectStatus(id, "contatado");
            setToast("Marcado como contatado.");
            loadProspects();
        } catch {
            setToast("Erro ao atualizar status.");
        }
    }

    async function handleDeleteProspect(id: number) {
        try {
            await deleteProspect(id);
            setToast("Prospect removido.");
            loadProspects();
        } catch {
            setToast("Erro ao remover.");
        }
    }

    async function handleCreateSchedule() {
        if (!schedForm.nicho) return;
        try {
            await createSchedule(schedForm);
            setToast("Agendamento criado.");
            setScheduleOpen(false);
            loadSchedules();
        } catch {
            setToast("Erro ao criar agendamento.");
        }
    }

    async function handleDeleteSchedule(id: number) {
        try {
            await deleteSchedule(id);
            setToast("Agendamento removido.");
            loadSchedules();
        } catch {
            setToast("Erro ao remover agendamento.");
        }
    }

    return (

        <Box>

            <Box sx={{ display: "flex", alignItems: "center", gap: 1.5, mb: 1 }}>
                <TravelExploreIcon sx={{ color: "#2563EB" }} />
                <Typography variant="h4" fontWeight="bold" color="#F8FAFC">
                    Prospecção de Nichos
                </Typography>
            </Box>

            <Typography color="#94A3B8" mb={3}>
                A IA analisa seus produtos, agrupa por nicho e classifica cada um como
                quente, morno ou frio — com dossiê e sugestão de abordagem.
            </Typography>

            <Tabs
                value={tab}
                onChange={(_, v) => setTab(v)}
                sx={{ mb: 3, borderBottom: "1px solid #1E293B" }}
            >
                <Tab label="Nichos Prospectados" sx={{ color: "#94A3B8" }} />
                <Tab label="Agendamentos" sx={{ color: "#94A3B8" }} />
            </Tabs>

            {tab === 0 && (
                <>
                    <Box sx={{ display: "flex", gap: 2, mb: 3, alignItems: "center" }}>
                        <TextField
                            size="small"
                            placeholder="Filtrar por nicho (ex: fone, camiseta...)"
                            value={nichoInput}
                            onChange={(e) => setNichoInput(e.target.value)}
                            sx={{
                                flex: 1,
                                "& .MuiInputBase-root": { backgroundColor: "#111827", color: "#F8FAFC" },
                                "& .MuiOutlinedInput-notchedOutline": { borderColor: "#1E293B" },
                            }}
                        />
                        <Button
                            variant="contained"
                            startIcon={<SearchIcon />}
                            onClick={handleScan}
                            disabled={loading}
                        >
                            Prospectar
                        </Button>
                    </Box>

                    {loading && (
                        <Box display="flex" justifyContent="center" py={6}>
                            <CircularProgress />
                        </Box>
                    )}

                    {!loading && error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}

                    {!loading && !error && prospects.length === 0 && (
                        <Alert severity="info">
                            Nenhum prospect ainda. Clique em "Prospectar" para a IA analisar seus produtos.
                        </Alert>
                    )}

                    <Grid container spacing={3}>
                        {prospects.map((p, idx) => (
                            <Grid item xs={12} md={6} lg={4} key={idx}>
                                <Card sx={{ backgroundColor: "#111827", borderRadius: 3, border: `1px solid ${tempColor(p.temperatura)}33` }}>
                                    <CardContent>
                                        <Box sx={{ display: "flex", justifyContent: "space-between", alignItems: "center", mb: 1.5 }}>
                                            <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
                                                {tempIcon(p.temperatura)}
                                                <Chip
                                                    label={p.temperatura.toUpperCase()}
                                                    size="small"
                                                    sx={{ backgroundColor: tempColor(p.temperatura), color: "#0B1120", fontWeight: 700 }}
                                                />
                                            </Box>
                                            <Chip
                                                label={`Score ${p.score}`}
                                                size="small"
                                                variant="outlined"
                                                sx={{ color: "#94A3B8", borderColor: "#1E293B" }}
                                            />
                                        </Box>

                                        <Typography fontWeight="bold" color="#F8FAFC" mb={1}>
                                            {p.nome}
                                        </Typography>

                                        <Box sx={{ display: "flex", gap: 2, mb: 1 }}>
                                            <Typography variant="caption" color="#94A3B8">
                                                {p.qtd_produtos} produto(s)
                                            </Typography>
                                            <Typography variant="caption" color="#94A3B8">
                                                R$ {p.preco_medio.toFixed(2)} preço médio
                                            </Typography>
                                        </Box>

                                        <Box sx={{ display: "flex", gap: 2, mb: 1 }}>
                                            <Typography variant="caption" color="#10B981">
                                                Comissão média: R$ {p.comissao_media.toFixed(2)}
                                            </Typography>
                                            <Typography variant="caption" color="#F59E0B">
                                                {p.vendas_total} vendas
                                            </Typography>
                                        </Box>

                                        <Divider sx={{ borderColor: "#1E293B", my: 1.5 }} />

                                        <Typography variant="body2" color="#94A3B8" sx={{ mb: 1 }}>
                                            {p.abordagem}
                                        </Typography>

                                        <Typography variant="caption" color="#2563EB" display="block" mb={2}>
                                            Canal: {p.canal_sugerido}
                                        </Typography>

                                        <Box sx={{ display: "flex", gap: 1 }}>
                                            {p.status !== "contatado" && (
                                                <Button
                                                    size="small"
                                                    variant="outlined"
                                                    onClick={() => handleContatado(p.id)}
                                                >
                                                    Marcar contatado
                                                </Button>
                                            )}
                                            <Button
                                                size="small"
                                                variant="outlined"
                                                color="error"
                                                startIcon={<DeleteIcon />}
                                                onClick={() => handleDeleteProspect(p.id)}
                                            >
                                                Remover
                                            </Button>
                                        </Box>
                                    </CardContent>
                                </Card>
                            </Grid>
                        ))}
                    </Grid>
                </>
            )}

            {tab === 1 && (
                <>
                    <Box sx={{ mb: 3 }}>
                        <Button
                            variant="contained"
                            startIcon={<ScheduleIcon />}
                            onClick={() => setScheduleOpen(true)}
                        >
                            Novo Agendamento
                        </Button>
                    </Box>

                    {loading && (
                        <Box display="flex" justifyContent="center" py={6}>
                            <CircularProgress />
                        </Box>
                    )}

                    {!loading && schedules.length === 0 && (
                        <Alert severity="info">
                            Nenhum agendamento. Crie um para a IA prospectar automaticamente no horário definido.
                        </Alert>
                    )}

                    <Grid container spacing={3}>
                        {schedules.map((s) => (
                            <Grid item xs={12} md={6} key={s.id}>
                                <Card sx={{ backgroundColor: "#111827", borderRadius: 3, border: "1px solid #1E293B" }}>
                                    <CardContent>
                                        <Typography fontWeight="bold" color="#F8FAFC" mb={1}>
                                            {s.nicho} {s.cidade ? `em ${s.cidade}` : ""}
                                        </Typography>
                                        <Typography variant="body2" color="#94A3B8">
                                            Horário: {s.hora} · Dias: {s.dias} · Qtd: {s.quantos}
                                        </Typography>
                                        <Typography variant="caption" color="#64748B" display="block" mb={2}>
                                            Última execução: {s.ultimo_run || "nunca"}
                                        </Typography>
                                        <Button
                                            size="small"
                                            variant="outlined"
                                            color="error"
                                            startIcon={<DeleteIcon />}
                                            onClick={() => handleDeleteSchedule(s.id)}
                                        >
                                            Remover
                                        </Button>
                                    </CardContent>
                                </Card>
                            </Grid>
                        ))}
                    </Grid>

                    <Dialog
                        open={scheduleOpen}
                        onClose={() => setScheduleOpen(false)}
                        PaperProps={{ sx: { backgroundColor: "#111827", color: "#F8FAFC" } }}
                    >
                        <DialogTitle>Novo Agendamento</DialogTitle>
                        <DialogContent sx={{ display: "flex", flexDirection: "column", gap: 2, pt: "16px !important", minWidth: 350 }}>
                            <TextField
                                label="Nicho"
                                size="small"
                                value={schedForm.nicho}
                                onChange={(e) => setSchedForm({ ...schedForm, nicho: e.target.value })}
                                InputLabelProps={{ sx: { color: "#94A3B8" } }}
                                sx={{ "& .MuiInputBase-root": { color: "#F8FAFC" }, "& .MuiOutlinedInput-notchedOutline": { borderColor: "#1E293B" } }}
                            />
                            <TextField
                                label="Horário (HH:MM)"
                                size="small"
                                value={schedForm.hora}
                                onChange={(e) => setSchedForm({ ...schedForm, hora: e.target.value })}
                                InputLabelProps={{ sx: { color: "#94A3B8" } }}
                                sx={{ "& .MuiInputBase-root": { color: "#F8FAFC" }, "& .MuiOutlinedInput-notchedOutline": { borderColor: "#1E293B" } }}
                            />
                            <TextField
                                label="Quantidade de leads"
                                size="small"
                                type="number"
                                value={schedForm.quantos}
                                onChange={(e) => setSchedForm({ ...schedForm, quantos: Number(e.target.value) })}
                                InputLabelProps={{ sx: { color: "#94A3B8" } }}
                                sx={{ "& .MuiInputBase-root": { color: "#F8FAFC" }, "& .MuiOutlinedInput-notchedOutline": { borderColor: "#1E293B" } }}
                            />
                        </DialogContent>
                        <DialogActions>
                            <Button onClick={() => setScheduleOpen(false)} sx={{ color: "#94A3B8" }}>
                                Cancelar
                            </Button>
                            <Button variant="contained" onClick={handleCreateSchedule}>
                                Criar
                            </Button>
                        </DialogActions>
                    </Dialog>
                </>
            )}

            <Snackbar
                open={!!toast}
                autoHideDuration={3000}
                onClose={() => setToast("")}
                message={toast}
            />

        </Box>

    );

}
