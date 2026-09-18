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
    Switch,
    Dialog,
    DialogTitle,
    DialogContent,
    DialogActions,
    TextField,
    MenuItem,
    Snackbar,
    IconButton,
    Grid,
} from "@mui/material";

import AddIcon from "@mui/icons-material/Add";
import DeleteIcon from "@mui/icons-material/Delete";
import PlayArrowIcon from "@mui/icons-material/PlayArrow";
import BoltIcon from "@mui/icons-material/Bolt";

import {
    getDefinitions,
    listRules,
    createRule,
    updateRule,
    deleteRule,
    runAutomation,
    type AutomationRuleItem,
    type DefinitionItem,
} from "../../services/automationService";

export default function Automation() {
    const [rules, setRules] = useState<AutomationRuleItem[]>([]);
    const [triggers, setTriggers] = useState<DefinitionItem[]>([]);
    const [actions, setActions] = useState<DefinitionItem[]>([]);
    const [loading, setLoading] = useState(false);
    const [running, setRunning] = useState(false);
    const [error, setError] = useState("");
    const [toast, setToast] = useState("");
    const [dialogOpen, setDialogOpen] = useState(false);

    const [form, setForm] = useState({
        name: "",
        trigger_type: "",
        action_type: "",
        days: "3",
        message: "",
        priority: "MEDIUM",
        status: "",
        temperatura: "",
    });

    async function load() {
        try {
            setLoading(true);
            const [def, r] = await Promise.all([getDefinitions(), listRules()]);
            setTriggers(def.triggers);
            setActions(def.actions);
            setRules(r);
        } catch {
            setError("Erro ao carregar automações.");
        } finally {
            setLoading(false);
        }
    }

    useEffect(() => { load(); }, []);

    async function handleCreate() {
        if (!form.name || !form.trigger_type || !form.action_type) return;

        const trigger_config: Record<string, any> = {};
        if (["card_stale", "prospect_cold"].includes(form.trigger_type)) {
            trigger_config.days = Number(form.days);
        }

        const action_config: Record<string, any> = {};
        if (form.action_type === "create_follow_up") {
            action_config.message = form.message;
            action_config.priority = form.priority;
        } else if (form.action_type === "change_prospect_status") {
            action_config.status = form.status;
        } else if (form.action_type === "change_prospect_temperature") {
            action_config.temperatura = form.temperatura;
        } else if (form.action_type === "notify") {
            action_config.message = form.message;
        }

        try {
            await createRule({
                name: form.name,
                trigger_type: form.trigger_type,
                trigger_config,
                action_type: form.action_type,
                action_config,
            });
            setDialogOpen(false);
            setToast("Regra criada!");
            load();
        } catch {
            setError("Erro ao criar regra.");
        }
    }

    async function handleToggle(id: number, current: boolean) {
        await updateRule(id, { is_enabled: !current });
        load();
    }

    async function handleDelete(id: number) {
        await deleteRule(id);
        setToast("Removida.");
        load();
    }

    async function handleRun() {
        try {
            setRunning(true);
            const result = await runAutomation();
            setToast(`${result.total} ação(ões) executada(s)!`);
            load();
        } catch {
            setError("Erro ao executar automações.");
        } finally {
            setRunning(false);
        }
    }

    function triggerName(id: string) {
        return triggers.find((t) => t.id === id)?.name || id;
    }
    function actionName(id: string) {
        return actions.find((a) => a.id === id)?.name || id;
    }

    return (
        <Box>
            <Box sx={{ display: "flex", justifyContent: "space-between", mb: 3, flexWrap: "wrap", gap: 1 }}>
                <Box>
                    <Typography variant="h5" fontWeight="bold" color="#F8FAFC">
                        Regras de Automação
                    </Typography>
                    <Typography variant="body2" color="#94A3B8">
                        Motor QUANDO / SE / ENTÃO — "nada morre no silêncio"
                    </Typography>
                </Box>
                <Box sx={{ display: "flex", gap: 1 }}>
                    <Button variant="outlined" startIcon={<PlayArrowIcon />} onClick={handleRun} disabled={running} sx={{ borderColor: "#10B981", color: "#10B981" }}>
                        {running ? "Executando..." : "Executar Agora"}
                    </Button>
                    <Button variant="contained" startIcon={<AddIcon />} onClick={() => setDialogOpen(true)} sx={{ backgroundColor: "#2563EB" }}>
                        Nova Regra
                    </Button>
                </Box>
            </Box>

            {error && <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError("")}>{error}</Alert>}

            {loading ? (
                <Box sx={{ display: "flex", justifyContent: "center", pt: 6 }}><CircularProgress sx={{ color: "#F97316" }} /></Box>
            ) : rules.length === 0 ? (
                <Typography color="#94A3B8">Nenhuma regra criada. Crie a primeira para automatizar seu funil.</Typography>
            ) : (
                <Grid container spacing={2}>
                    {rules.map((rule) => (
                        <Grid item xs={12} sm={6} md={4} key={rule.id}>
                            <Card sx={{ backgroundColor: "#0F172A", border: "1px solid #334155", height: "100%" }}>
                                <CardContent>
                                    <Box sx={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", mb: 1 }}>
                                        <Box sx={{ display: "flex", alignItems: "center", gap: 0.5 }}>
                                            <BoltIcon sx={{ fontSize: 16, color: "#F59E0B" }} />
                                            <Typography variant="body1" color="#F8FAFC" fontWeight={600}>{rule.name}</Typography>
                                        </Box>
                                        <Switch checked={rule.is_enabled} onChange={() => handleToggle(rule.id, rule.is_enabled)} size="small" />
                                    </Box>
                                    <Typography variant="caption" color="#64748B">QUANDO</Typography>
                                    <Typography variant="body2" color="#3B82F6" sx={{ mb: 1 }}>{triggerName(rule.trigger_type)}</Typography>
                                    <Typography variant="caption" color="#64748B">ENTÃO</Typography>
                                    <Typography variant="body2" color="#10B981" sx={{ mb: 1 }}>{actionName(rule.action_type)}</Typography>
                                    <Box sx={{ display: "flex", gap: 0.5, mt: 1 }}>
                                        <Chip label={`${rule.trigger_count} disparo(s)`} size="small" sx={{ height: 20, fontSize: 10, backgroundColor: "#1E293B", color: "#94A3B8" }} />
                                        <IconButton size="small" onClick={() => handleDelete(rule.id)} sx={{ color: "#EF4444", ml: "auto" }}><DeleteIcon fontSize="small" /></IconButton>
                                    </Box>
                                </CardContent>
                            </Card>
                        </Grid>
                    ))}
                </Grid>
            )}

            <Dialog open={dialogOpen} onClose={() => setDialogOpen(false)} maxWidth="sm" fullWidth PaperProps={{ sx: { backgroundColor: "#0F172A", color: "#F8FAFC" } }}>
                <DialogTitle>Nova Regra de Automação</DialogTitle>
                <DialogContent sx={{ display: "flex", flexDirection: "column", gap: 2, pt: "8px !important" }}>
                    <TextField label="Nome da regra" value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} InputLabelProps={{ sx: { color: "#94A3B8" } }} InputProps={{ sx: { color: "#F8FAFC" } }} />

                    <TextField select label="QUANDO (Gatilho)" value={form.trigger_type} onChange={(e) => setForm({ ...form, trigger_type: e.target.value })} InputLabelProps={{ sx: { color: "#94A3B8" } }} InputProps={{ sx: { color: "#F8FAFC" } }}>
                        {triggers.map((t) => <MenuItem key={t.id} value={t.id}>{t.name}</MenuItem>)}
                    </TextField>

                    {["card_stale", "prospect_cold"].includes(form.trigger_type) && (
                        <TextField label="Dias" type="number" value={form.days} onChange={(e) => setForm({ ...form, days: e.target.value })} InputLabelProps={{ sx: { color: "#94A3B8" } }} InputProps={{ sx: { color: "#F8FAFC" } }} />
                    )}

                    <TextField select label="ENTÃO (Ação)" value={form.action_type} onChange={(e) => setForm({ ...form, action_type: e.target.value })} InputLabelProps={{ sx: { color: "#94A3B8" } }} InputProps={{ sx: { color: "#F8FAFC" } }}>
                        {actions.map((a) => <MenuItem key={a.id} value={a.id}>{a.name}</MenuItem>)}
                    </TextField>

                    {(form.action_type === "create_follow_up" || form.action_type === "notify") && (
                        <TextField label="Mensagem" value={form.message} onChange={(e) => setForm({ ...form, message: e.target.value })} multiline rows={2} InputLabelProps={{ sx: { color: "#94A3B8" } }} InputProps={{ sx: { color: "#F8FAFC" } }} />
                    )}
                    {form.action_type === "create_follow_up" && (
                        <TextField select label="Prioridade" value={form.priority} onChange={(e) => setForm({ ...form, priority: e.target.value })} InputLabelProps={{ sx: { color: "#94A3B8" } }} InputProps={{ sx: { color: "#F8FAFC" } }}>
                            <MenuItem value="HIGH">Alta</MenuItem>
                            <MenuItem value="MEDIUM">Média</MenuItem>
                            <MenuItem value="LOW">Baixa</MenuItem>
                        </TextField>
                    )}
                    {form.action_type === "change_prospect_status" && (
                        <TextField label="Novo status" value={form.status} onChange={(e) => setForm({ ...form, status: e.target.value })} InputLabelProps={{ sx: { color: "#94A3B8" } }} InputProps={{ sx: { color: "#F8FAFC" } }} />
                    )}
                    {form.action_type === "change_prospect_temperature" && (
                        <TextField select label="Nova temperatura" value={form.temperatura} onChange={(e) => setForm({ ...form, temperatura: e.target.value })} InputLabelProps={{ sx: { color: "#94A3B8" } }} InputProps={{ sx: { color: "#F8FAFC" } }}>
                            <MenuItem value="quente">Quente</MenuItem>
                            <MenuItem value="morno">Morno</MenuItem>
                            <MenuItem value="frio">Frio</MenuItem>
                        </TextField>
                    )}
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
