import { useEffect, useState } from "react";

import {
    Box,
    Typography,
    Card,
    CardContent,
    Button,
    CircularProgress,
    Alert,
    TextField,
    Grid,
    Switch,
    FormControlLabel,
    MenuItem,
    Snackbar,
    Divider,
} from "@mui/material";

import SaveIcon from "@mui/icons-material/Save";
import SendIcon from "@mui/icons-material/Send";

import {
    getAIAgentConfig,
    updateAIAgentConfig,
    testAIAgent,
    PROVIDER_MODELS,
    type AIAgentConfig as AIAgentConfigType,
} from "../../services/aiAgentService";

export default function AIAgent() {
    const [form, setForm] = useState<AIAgentConfigType | null>(null);
    const [loading, setLoading] = useState(false);
    const [saving, setSaving] = useState(false);
    const [error, setError] = useState("");
    const [toast, setToast] = useState("");

    const [testMessage, setTestMessage] = useState("Oi, quanto custa o produto?");
    const [testReply, setTestReply] = useState("");
    const [testError, setTestError] = useState("");
    const [testing, setTesting] = useState(false);

    async function load() {
        try {
            setLoading(true);
            const cfg = await getAIAgentConfig();
            setForm(cfg);
        } catch {
            setError("Erro ao carregar configuração do agente de IA.");
        } finally {
            setLoading(false);
        }
    }

    useEffect(() => { load(); }, []);

    async function handleSave() {
        if (!form) return;
        try {
            setSaving(true);
            const updated = await updateAIAgentConfig({
                is_enabled: form.is_enabled,
                auto_reply_whatsapp: form.auto_reply_whatsapp,
                provider: form.provider,
                model_name: form.model_name,
                system_prompt: form.system_prompt,
            });
            setForm(updated);
            setToast("Configuração salva!");
        } catch {
            setError("Erro ao salvar configuração.");
        } finally {
            setSaving(false);
        }
    }

    async function handleTest() {
        try {
            setTesting(true);
            setTestError("");
            setTestReply("");
            const result = await testAIAgent(testMessage);
            setTestReply(result.reply);
        } catch (e: any) {
            setTestError(e?.response?.data?.message || "Falha ao testar o agente de IA.");
        } finally {
            setTesting(false);
        }
    }

    if (loading || !form) {
        return <Box sx={{ display: "flex", justifyContent: "center", pt: 10 }}><CircularProgress sx={{ color: "#F97316" }} /></Box>;
    }

    return (
        <Box>
            <Typography variant="h5" fontWeight="bold" color="#F8FAFC" gutterBottom>
                Agente de IA
            </Typography>
            <Typography variant="body2" color="#94A3B8" sx={{ mb: 3 }}>
                Configure o agente que pode responder automaticamente as conversas do WhatsApp.
            </Typography>

            {error && <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError("")}>{error}</Alert>}

            {!form.provider_configured && (
                <Alert severity="warning" sx={{ mb: 3 }}>
                    O provedor selecionado (<b>{form.provider}</b>) ainda não tem uma chave de API configurada no servidor (.env).
                    O agente não vai gerar respostas até que uma chave válida seja adicionada (OPENROUTER_API_KEY, OPENAI_API_KEY ou ANTHROPIC_API_KEY).
                </Alert>
            )}

            <Card sx={{ backgroundColor: "#0F172A", border: "1px solid #334155", mb: 3 }}>
                <CardContent>
                    <Grid container spacing={2}>
                        <Grid item xs={12} sm={6}>
                            <FormControlLabel
                                control={
                                    <Switch
                                        checked={form.is_enabled}
                                        onChange={(e) => setForm({ ...form, is_enabled: e.target.checked })}
                                        sx={{ "& .MuiSwitch-switchBase.Mui-checked": { color: "#F97316" } }}
                                    />
                                }
                                label={<Typography color="#F8FAFC">Agente Ativo</Typography>}
                            />
                        </Grid>
                        <Grid item xs={12} sm={6}>
                            <FormControlLabel
                                control={
                                    <Switch
                                        checked={form.auto_reply_whatsapp}
                                        onChange={(e) => setForm({ ...form, auto_reply_whatsapp: e.target.checked })}
                                        sx={{ "& .MuiSwitch-switchBase.Mui-checked": { color: "#F97316" } }}
                                    />
                                }
                                label={<Typography color="#F8FAFC">Responder automaticamente no WhatsApp</Typography>}
                            />
                        </Grid>

                        <Grid item xs={12} sm={6}>
                            <TextField
                                select
                                fullWidth
                                label="Provedor de IA"
                                value={form.provider}
                                onChange={(e) => {
                                    const newProvider = e.target.value;
                                    const defaultModel = (PROVIDER_MODELS[newProvider] || [""])[0];
                                    setForm({ ...form, provider: newProvider, model_name: defaultModel });
                                }}
                                InputLabelProps={{ sx: { color: "#94A3B8" } }}
                                InputProps={{ sx: { color: "#F8FAFC" } }}
                            >
                                {form.providers_disponiveis.map((p) => (
                                    <MenuItem key={p} value={p}>{p}</MenuItem>
                                ))}
                            </TextField>
                        </Grid>
                        <Grid item xs={12} sm={6}>
                            <TextField
                                select
                                fullWidth
                                label="Modelo"
                                value={form.model_name}
                                onChange={(e) => setForm({ ...form, model_name: e.target.value })}
                                InputLabelProps={{ sx: { color: "#94A3B8" } }}
                                InputProps={{ sx: { color: "#F8FAFC" } }}
                            >
                                {(PROVIDER_MODELS[form.provider] || []).map((m) => (
                                    <MenuItem key={m} value={m}>{m}</MenuItem>
                                ))}
                            </TextField>
                        </Grid>

                        <Grid item xs={12}>
                            <TextField
                                fullWidth
                                multiline
                                minRows={4}
                                label="Prompt de Sistema (personalidade do agente)"
                                value={form.system_prompt}
                                onChange={(e) => setForm({ ...form, system_prompt: e.target.value })}
                                InputLabelProps={{ sx: { color: "#94A3B8" } }}
                                InputProps={{ sx: { color: "#F8FAFC" } }}
                            />
                        </Grid>
                    </Grid>

                    <Button
                        variant="contained"
                        startIcon={<SaveIcon />}
                        onClick={handleSave}
                        disabled={saving}
                        sx={{ mt: 3, backgroundColor: "#F97316", "&:hover": { backgroundColor: "#EA580C" } }}
                    >
                        {saving ? "Salvando..." : "Salvar Configuração"}
                    </Button>
                </CardContent>
            </Card>

            <Card sx={{ backgroundColor: "#0F172A", border: "1px solid #334155" }}>
                <CardContent>
                    <Typography variant="subtitle1" color="#F8FAFC" gutterBottom>
                        Testar Agente
                    </Typography>
                    <Typography variant="body2" color="#94A3B8" sx={{ mb: 2 }}>
                        Envie uma mensagem de teste (não é enviada pelo WhatsApp de verdade).
                    </Typography>

                    <TextField
                        fullWidth
                        label="Mensagem de teste"
                        value={testMessage}
                        onChange={(e) => setTestMessage(e.target.value)}
                        InputLabelProps={{ sx: { color: "#94A3B8" } }}
                        InputProps={{ sx: { color: "#F8FAFC" } }}
                        sx={{ mb: 2 }}
                    />

                    <Button
                        variant="outlined"
                        startIcon={<SendIcon />}
                        onClick={handleTest}
                        disabled={testing}
                        sx={{ color: "#2563EB", borderColor: "#2563EB" }}
                    >
                        {testing ? "Enviando..." : "Testar"}
                    </Button>

                    {testError && <Alert severity="error" sx={{ mt: 2 }}>{testError}</Alert>}

                    {testReply && (
                        <>
                            <Divider sx={{ my: 2, borderColor: "#334155" }} />
                            <Typography variant="body2" color="#94A3B8">Resposta do agente:</Typography>
                            <Typography color="#F8FAFC">{testReply}</Typography>
                        </>
                    )}
                </CardContent>
            </Card>

            <Snackbar open={!!toast} autoHideDuration={3000} onClose={() => setToast("")} message={toast} />
        </Box>
    );
}
