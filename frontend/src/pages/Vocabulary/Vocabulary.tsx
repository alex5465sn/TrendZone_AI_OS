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
    Chip,
    Snackbar,
} from "@mui/material";

import SaveIcon from "@mui/icons-material/Save";

import {
    getVocabulary,
    getPresets,
    updateVocabulary,
    type VocabularyConfig,
} from "../../services/vocabularyService";

export default function Vocabulary() {
    const [form, setForm] = useState<VocabularyConfig | null>(null);
    const [presets, setPresets] = useState<Record<string, VocabularyConfig>>({});
    const [loading, setLoading] = useState(false);
    const [saving, setSaving] = useState(false);
    const [error, setError] = useState("");
    const [toast, setToast] = useState("");

    async function load() {
        try {
            setLoading(true);
            const [v, p] = await Promise.all([getVocabulary(), getPresets()]);
            setForm(v);
            setPresets(p);
        } catch {
            setError("Erro ao carregar vocabulário.");
        } finally {
            setLoading(false);
        }
    }

    useEffect(() => { load(); }, []);

    async function handleSave() {
        if (!form) return;
        try {
            setSaving(true);
            await updateVocabulary(form);
            setToast("Vocabulário salvo!");
        } catch {
            setError("Erro ao salvar.");
        } finally {
            setSaving(false);
        }
    }

    function applyPreset(key: string) {
        setForm(presets[key]);
    }

    if (loading || !form) {
        return <Box sx={{ display: "flex", justifyContent: "center", pt: 10 }}><CircularProgress sx={{ color: "#F97316" }} /></Box>;
    }

    const fields: { key: keyof VocabularyConfig; label: string }[] = [
        { key: "niche_name", label: "Nome do Nicho" },
        { key: "term_lead", label: "Termo para 'Lead'" },
        { key: "term_prospect", label: "Termo para 'Prospect'" },
        { key: "term_customer", label: "Termo para 'Cliente'" },
        { key: "term_deal", label: "Termo para 'Oportunidade'" },
        { key: "term_hot", label: "Termo para 'Quente'" },
        { key: "term_cold", label: "Termo para 'Frio'" },
    ];

    return (
        <Box>
            <Typography variant="h5" fontWeight="bold" color="#F8FAFC" gutterBottom>
                Vocabulário do Nicho
            </Typography>
            <Typography variant="body2" color="#94A3B8" sx={{ mb: 3 }}>
                Personalize os termos usados na plataforma para o seu segmento (ex: Lead/Paciente/Comprador)
            </Typography>

            {error && <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError("")}>{error}</Alert>}

            <Box sx={{ mb: 3, display: "flex", gap: 1, flexWrap: "wrap" }}>
                {Object.entries(presets).map(([key, preset]) => (
                    <Chip
                        key={key}
                        label={preset.niche_name}
                        onClick={() => applyPreset(key)}
                        sx={{ backgroundColor: "#1E293B", color: "#F8FAFC", cursor: "pointer", "&:hover": { backgroundColor: "#334155" } }}
                    />
                ))}
            </Box>

            <Card sx={{ backgroundColor: "#0F172A", border: "1px solid #334155" }}>
                <CardContent>
                    <Grid container spacing={2}>
                        {fields.map((f) => (
                            <Grid item xs={12} sm={6} key={f.key}>
                                <TextField
                                    fullWidth
                                    label={f.label}
                                    value={form[f.key]}
                                    onChange={(e) => setForm({ ...form, [f.key]: e.target.value })}
                                    InputLabelProps={{ sx: { color: "#94A3B8" } }}
                                    InputProps={{ sx: { color: "#F8FAFC" } }}
                                />
                            </Grid>
                        ))}
                    </Grid>
                    <Button
                        variant="contained"
                        startIcon={<SaveIcon />}
                        onClick={handleSave}
                        disabled={saving}
                        sx={{ mt: 3, backgroundColor: "#F97316", "&:hover": { backgroundColor: "#EA580C" } }}
                    >
                        {saving ? "Salvando..." : "Salvar Vocabulário"}
                    </Button>
                </CardContent>
            </Card>

            <Snackbar open={!!toast} autoHideDuration={3000} onClose={() => setToast("")} message={toast} />
        </Box>
    );
}
