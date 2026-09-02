import { useEffect, useState } from "react";

import {
    Box,
    Typography,
    Grid,
    Card,
    CardContent,
    CardMedia,
    Chip,
    Button,
    CircularProgress,
    Alert,
    Divider,
    Tabs,
    Tab,
    Snackbar,
} from "@mui/material";

import ContentCopyIcon from "@mui/icons-material/ContentCopy";
import SaveIcon from "@mui/icons-material/Save";
import CheckCircleIcon from "@mui/icons-material/CheckCircle";
import DeleteIcon from "@mui/icons-material/Delete";
import CampaignIcon from "@mui/icons-material/Campaign";

import {
    getOpportunities,
    saveCampaign,
    listCampaigns,
    publishCampaign,
    deleteCampaign,
    type Opportunity,
    type Campaign,
} from "../../services/opportunityService";

function decisionColor(decision: string) {
    if (decision === "PROMOVER") return "#10B981";
    if (decision === "TESTAR") return "#F59E0B";
    return "#94A3B8";
}

export default function Opportunities() {

    const [tab, setTab] = useState(0);
    const [opportunities, setOpportunities] = useState<Opportunity[]>([]);
    const [campaigns, setCampaigns] = useState<Campaign[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");
    const [toast, setToast] = useState("");

    async function loadOpportunities() {
        try {
            setLoading(true);
            const data = await getOpportunities(10);
            setOpportunities(data);
        } catch (err) {
            console.error(err);
            setError("Erro ao carregar oportunidades.");
        } finally {
            setLoading(false);
        }
    }

    async function loadCampaigns() {
        try {
            setLoading(true);
            const data = await listCampaigns();
            setCampaigns(data);
        } catch (err) {
            console.error(err);
            setError("Erro ao carregar campanhas.");
        } finally {
            setLoading(false);
        }
    }

    useEffect(() => {
        if (tab === 0) {
            loadOpportunities();
        } else {
            loadCampaigns();
        }
    }, [tab]);

    async function handleSave(op: Opportunity) {
        try {
            await saveCampaign({
                product_id: op.product.id,
                title: op.content.title,
                caption: op.content.caption,
                hashtags: op.content.hashtags,
                target_audience: op.content.target_audience,
                channel: op.content.channel,
            });
            setToast("Campanha salva como rascunho.");
        } catch (err) {
            console.error(err);
            setToast("Erro ao salvar campanha.");
        }
    }

    async function handleCopy(op: Opportunity) {
        const text = `${op.content.title}\n\n${op.content.caption}\n\n${op.content.hashtags}\n\n${op.product.offer_link}`;
        await navigator.clipboard.writeText(text);
        setToast("Conteúdo copiado para a área de transferência.");
    }

    async function handlePublish(id: number) {
        try {
            await publishCampaign(id);
            setToast("Campanha marcada como publicada.");
            loadCampaigns();
        } catch (err) {
            console.error(err);
            setToast("Erro ao publicar campanha.");
        }
    }

    async function handleDelete(id: number) {
        try {
            await deleteCampaign(id);
            setToast("Campanha removida.");
            loadCampaigns();
        } catch (err) {
            console.error(err);
            setToast("Erro ao remover campanha.");
        }
    }

    return (

        <Box>

            <Box sx={{ display: "flex", alignItems: "center", gap: 1.5, mb: 1 }}>
                <CampaignIcon sx={{ color: "#2563EB" }} />
                <Typography variant="h4" fontWeight="bold" color="#F8FAFC">
                    Oportunidades de Venda
                </Typography>
            </Box>

            <Typography color="#94A3B8" mb={4}>
                A IA analisa os produtos monitorados e sugere conteúdo de divulgação pronto.
                Você revisa, copia ou salva e publica manualmente onde preferir.
            </Typography>

            <Tabs
                value={tab}
                onChange={(_, v) => setTab(v)}
                sx={{ mb: 3, borderBottom: "1px solid #1E293B" }}
            >
                <Tab label="Sugestões da IA" sx={{ color: "#94A3B8" }} />
                <Tab label="Campanhas Salvas" sx={{ color: "#94A3B8" }} />
            </Tabs>

            {loading && (
                <Box display="flex" justifyContent="center" py={6}>
                    <CircularProgress />
                </Box>
            )}

            {!loading && error && (
                <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>
            )}

            {!loading && !error && tab === 0 && (

                <Grid container spacing={3}>

                    {opportunities.length === 0 && (
                        <Grid item xs={12}>
                            <Alert severity="info">
                                Nenhuma oportunidade encontrada no momento. À medida que o Scout IA
                                encontrar produtos com Score mais alto, elas aparecerão aqui.
                            </Alert>
                        </Grid>
                    )}

                    {opportunities.map((op, idx) => (
                        <Grid item xs={12} md={6} key={idx}>
                            <Card sx={{ backgroundColor: "#111827", borderRadius: 3, border: "1px solid #1E293B" }}>
                                {op.product.image && (
                                    <CardMedia
                                        component="img"
                                        image={op.product.image}
                                        alt={op.product.name}
                                        sx={{ height: 160, objectFit: "cover" }}
                                    />
                                )}
                                <CardContent>
                                    <Box sx={{ display: "flex", justifyContent: "space-between", alignItems: "center", mb: 1 }}>
                                        <Chip
                                            label={op.decision}
                                            size="small"
                                            sx={{ backgroundColor: decisionColor(op.decision), color: "#0B1120", fontWeight: 700 }}
                                        />
                                        <Chip
                                            label={`Score ${op.product.score.toFixed(0)}`}
                                            size="small"
                                            variant="outlined"
                                            sx={{ color: "#94A3B8", borderColor: "#1E293B" }}
                                        />
                                    </Box>

                                    <Typography fontWeight="bold" color="#F8FAFC" mb={1}>
                                        {op.content.title}
                                    </Typography>

                                    <Typography
                                        variant="body2"
                                        color="#94A3B8"
                                        sx={{ whiteSpace: "pre-line", mb: 1 }}
                                    >
                                        {op.content.caption}
                                    </Typography>

                                    <Typography variant="caption" color="#2563EB" display="block" mb={1}>
                                        {op.content.hashtags}
                                    </Typography>

                                    <Divider sx={{ borderColor: "#1E293B", my: 1.5 }} />

                                    <Typography variant="caption" color="#94A3B8" display="block">
                                        Público-alvo: {op.content.target_audience}
                                    </Typography>
                                    <Typography variant="caption" color="#94A3B8" display="block" mb={2}>
                                        Canal sugerido: {op.content.channel}
                                    </Typography>

                                    <Box sx={{ display: "flex", gap: 1 }}>
                                        <Button
                                            size="small"
                                            variant="outlined"
                                            startIcon={<ContentCopyIcon />}
                                            onClick={() => handleCopy(op)}
                                        >
                                            Copiar
                                        </Button>
                                        <Button
                                            size="small"
                                            variant="contained"
                                            startIcon={<SaveIcon />}
                                            onClick={() => handleSave(op)}
                                        >
                                            Salvar
                                        </Button>
                                    </Box>
                                </CardContent>
                            </Card>
                        </Grid>
                    ))}

                </Grid>

            )}

            {!loading && !error && tab === 1 && (

                <Grid container spacing={3}>

                    {campaigns.length === 0 && (
                        <Grid item xs={12}>
                            <Alert severity="info">Nenhuma campanha salva ainda.</Alert>
                        </Grid>
                    )}

                    {campaigns.map((c) => (
                        <Grid item xs={12} md={6} key={c.id}>
                            <Card sx={{ backgroundColor: "#111827", borderRadius: 3, border: "1px solid #1E293B" }}>
                                <CardContent>
                                    <Box sx={{ display: "flex", justifyContent: "space-between", mb: 1 }}>
                                        <Chip
                                            label={c.status}
                                            size="small"
                                            sx={{
                                                backgroundColor: c.status === "PUBLISHED" ? "#10B981" : "#F59E0B",
                                                color: "#0B1120",
                                                fontWeight: 700,
                                            }}
                                        />
                                    </Box>

                                    <Typography fontWeight="bold" color="#F8FAFC" mb={1}>
                                        {c.title}
                                    </Typography>

                                    <Typography variant="body2" color="#94A3B8" sx={{ whiteSpace: "pre-line", mb: 1 }}>
                                        {c.caption}
                                    </Typography>

                                    <Typography variant="caption" color="#2563EB" display="block" mb={2}>
                                        {c.hashtags}
                                    </Typography>

                                    <Box sx={{ display: "flex", gap: 1 }}>
                                        {c.status !== "PUBLISHED" && (
                                            <Button
                                                size="small"
                                                variant="contained"
                                                color="success"
                                                startIcon={<CheckCircleIcon />}
                                                onClick={() => handlePublish(c.id)}
                                            >
                                                Marcar publicada
                                            </Button>
                                        )}
                                        <Button
                                            size="small"
                                            variant="outlined"
                                            color="error"
                                            startIcon={<DeleteIcon />}
                                            onClick={() => handleDelete(c.id)}
                                        >
                                            Remover
                                        </Button>
                                    </Box>
                                </CardContent>
                            </Card>
                        </Grid>
                    ))}

                </Grid>

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
