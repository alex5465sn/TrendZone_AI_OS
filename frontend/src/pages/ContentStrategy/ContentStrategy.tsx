import { useEffect, useState } from "react";

import {
    Box,
    Typography,
    Chip,
    Button,
    CircularProgress,
    Alert,
    Dialog,
    DialogTitle,
    DialogContent,
    DialogActions,
    TextField,
    MenuItem,
    Snackbar,
    IconButton,
    Accordion,
    AccordionSummary,
    AccordionDetails,
} from "@mui/material";

import AutoAwesomeIcon from "@mui/icons-material/AutoAwesome";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";
import DeleteIcon from "@mui/icons-material/Delete";
import ContentCopyIcon from "@mui/icons-material/ContentCopy";

import {
    generateStrategies,
    listStrategies,
    updateStrategyStatus,
    deleteStrategy,
    type ContentStrategyItem,
} from "../../services/contentStrategyService";
import { getProducts, type Product } from "../../services/productService";

const platformLabels: Record<string, string> = {
    shopee_video: "Shopee Vídeo",
    pinterest: "Pinterest",
    whatsapp: "WhatsApp",
    facebook: "Facebook",
    instagram: "Instagram",
    tiktok: "TikTok",
    blog: "Blog/SEO",
};

const platformColors: Record<string, string> = {
    shopee_video: "#EE4D2D",
    pinterest: "#E60023",
    whatsapp: "#25D366",
    facebook: "#1877F2",
    instagram: "#E4405F",
    tiktok: "#000000",
    blog: "#F97316",
};

const statusLabels: Record<string, string> = {
    DRAFT: "Rascunho",
    IN_PROGRESS: "Em Produção",
    PUBLISHED: "Publicado",
    ARCHIVED: "Arquivado",
};

export default function ContentStrategyPage() {
    const [items, setItems] = useState<ContentStrategyItem[]>([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");
    const [toast, setToast] = useState("");
    const [genDialog, setGenDialog] = useState(false);
    const [genProductId, setGenProductId] = useState("");
    const [genPlatforms, setGenPlatforms] = useState<string[]>(["shopee_video", "pinterest", "whatsapp"]);
    const [generating, setGenerating] = useState(false);
    const [filterPlatform, setFilterPlatform] = useState("");
    const [products, setProducts] = useState<Product[]>([]);

    async function openGenDialog(productId?: number) {
        try {
            const list = await getProducts();
            setProducts(list);
            setGenProductId(productId ? String(productId) : (list[0] ? String(list[0].id) : ""));
        } catch {
            setProducts([]);
        }
        setGenDialog(true);
    }

    async function load() {
        try {
            setLoading(true);
            const data = await listStrategies(filterPlatform || undefined);
            setItems(data);
        } catch {
            setError("Erro ao carregar estratégias.");
        } finally {
            setLoading(false);
        }
    }

    useEffect(() => { load(); }, [filterPlatform]);

    async function handleGenerate() {
        const pid = parseInt(genProductId);
        if (!pid || genPlatforms.length === 0) return;
        try {
            setGenerating(true);
            await generateStrategies(pid, genPlatforms);
            setGenDialog(false);
            setToast("Estratégias geradas!");
            load();
        } catch {
            setError("Erro ao gerar estratégias.");
        } finally {
            setGenerating(false);
        }
    }

    async function handleStatusChange(id: number, status: string) {
        await updateStrategyStatus(id, status);
        setToast("Status atualizado.");
        load();
    }

    async function handleDelete(id: number) {
        await deleteStrategy(id);
        setToast("Removido.");
        load();
    }

    function copyToClipboard(text: string) {
        navigator.clipboard.writeText(text);
        setToast("Copiado!");
    }

    return (
        <Box>
            <Box sx={{ display: "flex", justifyContent: "space-between", mb: 3 }}>
                <Box>
                    <Typography variant="h5" fontWeight="bold" color="#F8FAFC">
                        Estratégias de Conteúdo
                    </Typography>
                    <Typography variant="body2" color="#94A3B8">
                        Gere scripts prontos para vídeo, post e blog otimizados por plataforma
                    </Typography>
                </Box>
                <Button
                    variant="contained"
                    startIcon={<AutoAwesomeIcon />}
                    onClick={() => openGenDialog()}
                    sx={{ backgroundColor: "#F97316", "&:hover": { backgroundColor: "#EA580C" } }}
                >
                    Gerar Estratégias
                </Button>
            </Box>

            {error && <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError("")}>{error}</Alert>}

            <Box sx={{ mb: 2, display: "flex", gap: 1, flexWrap: "wrap" }}>
                <Chip
                    label="Todos"
                    onClick={() => setFilterPlatform("")}
                    sx={{ backgroundColor: !filterPlatform ? "#2563EB" : "#1E293B", color: "#F8FAFC", cursor: "pointer" }}
                />
                {Object.entries(platformLabels).map(([key, label]) => (
                    <Chip
                        key={key}
                        label={label}
                        onClick={() => setFilterPlatform(key)}
                        sx={{
                            backgroundColor: filterPlatform === key ? platformColors[key] : "#1E293B",
                            color: "#F8FAFC",
                            cursor: "pointer",
                        }}
                    />
                ))}
            </Box>

            {loading ? (
                <Box sx={{ display: "flex", justifyContent: "center", pt: 6 }}><CircularProgress sx={{ color: "#F97316" }} /></Box>
            ) : items.length === 0 ? (
                <Typography color="#94A3B8">Nenhuma estratégia gerada ainda. Clique em "Gerar Estratégias" para começar.</Typography>
            ) : (
                <Box sx={{ display: "flex", flexDirection: "column", gap: 1.5 }}>
                    {items.map((item) => (
                        <Accordion
                            key={item.id}
                            sx={{ backgroundColor: "#0F172A", border: "1px solid #334155", "&:before": { display: "none" } }}
                        >
                            <AccordionSummary expandIcon={<ExpandMoreIcon sx={{ color: "#94A3B8" }} />}>
                                <Box sx={{ display: "flex", alignItems: "center", gap: 1, flex: 1 }}>
                                    <Chip
                                        label={platformLabels[item.platform] || item.platform}
                                        size="small"
                                        sx={{ backgroundColor: platformColors[item.platform] || "#64748B", color: "#fff", height: 22, fontSize: 11 }}
                                    />
                                    <Typography variant="body2" color="#F8FAFC" fontWeight={600} sx={{ flex: 1 }}>
                                        {item.title}
                                    </Typography>
                                    <Chip label={statusLabels[item.status] || item.status} size="small" sx={{ height: 20, fontSize: 10, backgroundColor: "#1E293B", color: "#94A3B8" }} />
                                </Box>
                            </AccordionSummary>
                            <AccordionDetails>
                                <Box sx={{ mb: 2 }}>
                                    <Typography variant="caption" color="#64748B" fontWeight={600}>SCRIPT / ROTEIRO</Typography>
                                    <Typography variant="body2" color="#CBD5E1" sx={{ whiteSpace: "pre-wrap", mt: 0.5, p: 1.5, backgroundColor: "#1E293B", borderRadius: 1 }}>
                                        {item.script}
                                    </Typography>
                                    <IconButton size="small" onClick={() => copyToClipboard(item.script)} sx={{ color: "#64748B", mt: 0.5 }}>
                                        <ContentCopyIcon fontSize="small" />
                                    </IconButton>
                                </Box>
                                {item.hashtags && (
                                    <Box sx={{ mb: 1 }}>
                                        <Typography variant="caption" color="#64748B" fontWeight={600}>HASHTAGS</Typography>
                                        <Typography variant="body2" color="#3B82F6">{item.hashtags}</Typography>
                                    </Box>
                                )}
                                {item.cta && (
                                    <Box sx={{ mb: 1 }}>
                                        <Typography variant="caption" color="#64748B" fontWeight={600}>CTA</Typography>
                                        <Typography variant="body2" color="#10B981">{item.cta}</Typography>
                                    </Box>
                                )}
                                {item.best_time && (
                                    <Box sx={{ mb: 1 }}>
                                        <Typography variant="caption" color="#64748B" fontWeight={600}>MELHORES HORÁRIOS</Typography>
                                        <Typography variant="body2" color="#F59E0B">{item.best_time}</Typography>
                                    </Box>
                                )}
                                <Box sx={{ display: "flex", gap: 1, mt: 2 }}>
                                    <Button size="small" variant="outlined" onClick={() => handleStatusChange(item.id, "IN_PROGRESS")} sx={{ borderColor: "#3B82F6", color: "#3B82F6" }}>Em Produção</Button>
                                    <Button size="small" variant="outlined" onClick={() => handleStatusChange(item.id, "PUBLISHED")} sx={{ borderColor: "#10B981", color: "#10B981" }}>Publicado</Button>
                                    <IconButton size="small" onClick={() => handleDelete(item.id)} sx={{ color: "#EF4444" }}><DeleteIcon fontSize="small" /></IconButton>
                                </Box>
                            </AccordionDetails>
                        </Accordion>
                    ))}
                </Box>
            )}

            <Dialog open={genDialog} onClose={() => setGenDialog(false)} maxWidth="sm" fullWidth PaperProps={{ sx: { backgroundColor: "#0F172A", color: "#F8FAFC" } }}>
                <DialogTitle>Gerar Estratégias de Conteúdo</DialogTitle>
                <DialogContent sx={{ display: "flex", flexDirection: "column", gap: 2, pt: "8px !important" }}>
                    <TextField
                        select
                        label="Produto"
                        value={genProductId}
                        onChange={(e) => setGenProductId(e.target.value)}
                        fullWidth
                        InputLabelProps={{ sx: { color: "#94A3B8" } }}
                        InputProps={{ sx: { color: "#F8FAFC" } }}
                        helperText={products.length === 0 ? "Nenhum produto rastreado ainda." : "Selecione o produto para gerar estratégias"}
                    >
                        {products.map((p) => (
                            <MenuItem key={p.id} value={String(p.id)}>{p.name}</MenuItem>
                        ))}
                    </TextField>
                    <Typography variant="body2" color="#94A3B8">Plataformas:</Typography>
                    <Box sx={{ display: "flex", gap: 1, flexWrap: "wrap" }}>
                        {Object.entries(platformLabels).map(([key, label]) => (
                            <Chip
                                key={key}
                                label={label}
                                onClick={() => {
                                    setGenPlatforms((prev) =>
                                        prev.includes(key) ? prev.filter((p) => p !== key) : [...prev, key]
                                    );
                                }}
                                sx={{
                                    backgroundColor: genPlatforms.includes(key) ? platformColors[key] : "#1E293B",
                                    color: "#F8FAFC",
                                    cursor: "pointer",
                                }}
                            />
                        ))}
                    </Box>
                </DialogContent>
                <DialogActions>
                    <Button onClick={() => setGenDialog(false)} sx={{ color: "#94A3B8" }}>Cancelar</Button>
                    <Button onClick={handleGenerate} variant="contained" disabled={generating} sx={{ backgroundColor: "#F97316" }}>
                        {generating ? <CircularProgress size={20} /> : "Gerar"}
                    </Button>
                </DialogActions>
            </Dialog>

            <Snackbar open={!!toast} autoHideDuration={3000} onClose={() => setToast("")} message={toast} />
        </Box>
    );
}
