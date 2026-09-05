import { useState } from "react";

import {
    Box,
    Typography,
    Paper,
    FormGroup,
    FormControlLabel,
    Checkbox,
    TextField,
    Button,
    Alert,
} from "@mui/material";

import { CATEGORIES } from "../../constants/categories";

interface AppSettings {
    favoriteCategories: string[];
    monthlySalesGoal: number;
    facebookPageName: string;
}

const STORAGE_KEY = "trendzone_settings";

function loadSettings(): AppSettings {
    try {
        const raw = localStorage.getItem(STORAGE_KEY);
        if (raw) return JSON.parse(raw);
    } catch {
        // ignora e usa padrão
    }
    return { favoriteCategories: [], monthlySalesGoal: 0, facebookPageName: "TrendZone" };
}

export default function Settings() {

    const [settings, setSettings] = useState<AppSettings>(loadSettings());
    const [saved, setSaved] = useState(false);

    function toggleCategory(id: string) {
        setSettings((prev) => ({
            ...prev,
            favoriteCategories: prev.favoriteCategories.includes(id)
                ? prev.favoriteCategories.filter((c) => c !== id)
                : [...prev.favoriteCategories, id],
        }));
    }

    function handleSave() {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(settings));
        setSaved(true);
        setTimeout(() => setSaved(false), 2500);
    }

    return (

        <Box>

            <Typography variant="h4" fontWeight="bold" color="#F8FAFC" mb={1}>
                Configurações
            </Typography>

            <Typography variant="body1" color="#94A3B8" mb={4}>
                Ajuste as preferências do Scout IA e do bot de divulgação.
            </Typography>

            {saved && (
                <Alert severity="success" sx={{ mb: 3 }}>
                    Configurações salvas.
                </Alert>
            )}

            <Paper sx={{ backgroundColor: "#111827", border: "1px solid #1E293B", borderRadius: 3, p: 3, mb: 3 }}>

                <Typography color="#F8FAFC" fontWeight="bold" mb={2}>
                    Categorias favoritas para o Scout IA
                </Typography>

                <Typography color="#94A3B8" fontSize="0.85rem" mb={2}>
                    O botão "Encontrar Produtos Campeões" vai priorizar essas categorias. Deixe tudo desmarcado para buscar em todas.
                </Typography>

                <FormGroup row>
                    {CATEGORIES.map((cat) => (
                        <FormControlLabel
                            key={cat.id}
                            control={
                                <Checkbox
                                    checked={settings.favoriteCategories.includes(cat.id)}
                                    onChange={() => toggleCategory(cat.id)}
                                    sx={{ color: "#94A3B8" }}
                                />
                            }
                            label={<Typography color="#F8FAFC">{cat.label}</Typography>}
                            sx={{ width: { xs: "100%", sm: "45%" } }}
                        />
                    ))}
                </FormGroup>

            </Paper>

            <Paper sx={{ backgroundColor: "#111827", border: "1px solid #1E293B", borderRadius: 3, p: 3, mb: 3 }}>

                <Typography color="#F8FAFC" fontWeight="bold" mb={2}>
                    Metas e divulgação
                </Typography>

                <TextField
                    label="Meta de vendas mensais (R$)"
                    type="number"
                    fullWidth
                    value={settings.monthlySalesGoal}
                    onChange={(e) => setSettings((prev) => ({ ...prev, monthlySalesGoal: Number(e.target.value) }))}
                    sx={{ mb: 2, input: { color: "#F8FAFC" } }}
                    InputLabelProps={{ style: { color: "#94A3B8" } }}
                />

                <TextField
                    label="Nome da página do Facebook"
                    fullWidth
                    value={settings.facebookPageName}
                    onChange={(e) => setSettings((prev) => ({ ...prev, facebookPageName: e.target.value }))}
                    helperText="Usado apenas como referência nos textos gerados pelo bot de divulgação."
                    sx={{ input: { color: "#F8FAFC" } }}
                    InputLabelProps={{ style: { color: "#94A3B8" } }}
                    FormHelperTextProps={{ style: { color: "#64748B" } }}
                />

            </Paper>

            <Button
                variant="contained"
                onClick={handleSave}
                sx={{ backgroundColor: "#8B5CF6", textTransform: "none", px: 4 }}
            >
                Salvar Configurações
            </Button>

        </Box>

    );

}
