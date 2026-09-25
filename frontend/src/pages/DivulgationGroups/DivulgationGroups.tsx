import { useEffect, useMemo, useState } from "react";

import {
    Box,
    Typography,
    Card,
    CardContent,
    Chip,
    Button,
    CircularProgress,
    Alert,
    TextField,
    MenuItem,
    Snackbar,
    IconButton,
    Grid,
    Stepper,
    Step,
    StepLabel,
    Dialog,
    DialogTitle,
    DialogContent,
    DialogActions,
    InputAdornment,
} from "@mui/material";

import ContentCopyIcon from "@mui/icons-material/ContentCopy";
import AutoAwesomeIcon from "@mui/icons-material/AutoAwesome";
import DeleteIcon from "@mui/icons-material/Delete";
import EditIcon from "@mui/icons-material/Edit";
import AddIcon from "@mui/icons-material/Add";
import SearchIcon from "@mui/icons-material/Search";
import WhatsAppIcon from "@mui/icons-material/WhatsApp";
import FacebookIcon from "@mui/icons-material/Facebook";
import AccessTimeIcon from "@mui/icons-material/AccessTime";
import OpenInNewIcon from "@mui/icons-material/OpenInNew";

import { getProducts, type Product } from "../../services/productService";
import {
    listDivulgationGroups,
    createDivulgationGroup,
    updateDivulgationGroup,
    deleteDivulgationGroup,
    generateDivulgationText,
    type DivulgationGroup,
    type GeneratedContent,
} from "../../services/divulgationGroupService";

const TONES = [
    { value: "oferta", label: "Oferta direta" },
    { value: "storytelling", label: "Storytelling" },
    { value: "humor", label: "Humor" },
    { value: "urgencia", label: "Urgência" },
];

const PLATFORM_FILTERS = [
    { value: "todos", label: "Todos" },
    { value: "whatsapp", label: "WhatsApp" },
    { value: "facebook", label: "Facebook" },
];

export default function DivulgationGroups() {
    const [products, setProducts] = useState<Product[]>([]);
    const [groups, setGroups] = useState<DivulgationGroup[]>([]);
    const [loading, setLoading] = useState(false);
    const [generating, setGenerating] = useState(false);
    const [error, setError] = useState("");
    const [toast, setToast] = useState("");

    const [productId, setProductId] = useState<number | "">("");
    const [tone, setTone] = useState("oferta");
    const [content, setContent] = useState<GeneratedContent | null>(null);

    const [platformFilter, setPlatformFilter] = useState("todos");
    const [search, setSearch] = useState("");

    const [dialogOpen, setDialogOpen] = useState(false);
    const [editingId, setEditingId] = useState<number | null>(null);
    const [form, setForm] = useState({
        name: "",
        platform: "whatsapp",
        category: "achadinhos",
        link: "",
        best_time: "",
        member_count: "0",
    });

    function openCreateDialog() {
        setEditingId(null);
        setForm({ name: "", platform: "whatsapp", category: "achadinhos", link: "", best_time: "", member_count: "0" });
        setDialogOpen(true);
    }

    function openEditDialog(g: DivulgationGroup) {
        setEditingId(g.id);
        setForm({
            name: g.name,
            platform: g.platform,
            category: g.category,
            link: g.link || "",
            best_time: g.best_time || "",
            member_count: String(g.member_count || 0),
        });
        setDialogOpen(true);
    }

    async function load() {
        try {
            setLoading(true);
            const [p, g] = await Promise.all([getProducts(), listDivulgationGroups()]);
            setProducts(p);
            setGroups(g);
        } catch {
            setError("Erro ao carregar produtos/grupos.");
        } finally {
            setLoading(false);
        }
    }

    useEffect(() => { load(); }, []);

    async function handleGenerate() {
        if (!productId) return;
        try {
            setGenerating(true);
            const result = await generateDivulgationText(Number(productId), tone);
            setContent(result);
        } catch {
            setError("Erro ao gerar texto com IA.");
        } finally {
            setGenerating(false);
        }
    }

    function fullText(): string {
        if (!content) return "";
        return `${content.caption}\n\n${content.hashtags}\n\n${content.link}`;
    }

    async function handleCopy() {
        try {
            await navigator.clipboard.writeText(fullText());
            setToast("Texto copiado! Agora é só colar no grupo.");
        } catch {
            setError("Não foi possível copiar automaticamente. Selecione e copie o texto manualmente.");
        }
    }

    async function handlePublish(g: DivulgationGroup) {
        if (!content) return;

        try {
            await navigator.clipboard.writeText(fullText());
        } catch {
            // Segue mesmo se o clipboard falhar - o link ainda abre.
        }

        if (g.link) {
            window.open(g.link, "_blank", "noopener,noreferrer");
            setToast(`Texto copiado! O grupo "${g.name}" foi aberto em outra aba — agora é só colar.`);
        } else {
            setToast("Texto copiado! Este grupo não tem link cadastrado, abra-o manualmente e cole.");
        }
    }

    async function handleSaveGroup() {
        if (!form.name) return;
        const payload = {
            name: form.name,
            platform: form.platform,
            category: form.category,
            link: form.link,
            best_time: form.best_time,
            member_count: Number(form.member_count) || 0,
        };
        try {
            if (editingId) {
                await updateDivulgationGroup(editingId, payload);
                setToast("Grupo atualizado!");
            } else {
                await createDivulgationGroup(payload);
                setToast("Grupo cadastrado!");
            }
            setDialogOpen(false);
            setEditingId(null);
            setForm({ name: "", platform: "whatsapp", category: "achadinhos", link: "", best_time: "", member_count: "0" });
            load();
        } catch {
            setError(editingId ? "Erro ao atualizar grupo." : "Erro ao cadastrar grupo.");
        }
    }

    async function handleDeleteGroup(id: number) {
        await deleteDivulgationGroup(id);
        setToast("Grupo removido.");
        load();
    }

    const filteredGroups = useMemo(() => {
        return groups.filter((g) => {
            const matchesPlatform = platformFilter === "todos" || g.platform === platformFilter;
            const matchesSearch = !search || g.name.toLowerCase().includes(search.toLowerCase()) || (g.category || "").toLowerCase().includes(search.toLowerCase());
            return matchesPlatform && matchesSearch;
        });
    }, [groups, platformFilter, search]);

    return (
        <Box>
            <Box sx={{ display: "flex", justifyContent: "space-between", mb: 1, flexWrap: "wrap", gap: 1 }}>
                <Box>
                    <Typography variant="h5" fontWeight="bold" color="#F8FAFC">
                        Grupos de Divulgação
                    </Typography>
                    <Typography variant="body2" color="#94A3B8">
                        Gere o texto com IA e publique manualmente nos seus grupos de WhatsApp e Facebook
                    </Typography>
                </Box>
                <Button variant="outlined" startIcon={<AddIcon />} onClick={openCreateDialog} sx={{ borderColor: "#334155", color: "#94A3B8" }}>
                    Cadastrar Grupo
                </Button>
            </Box>

            <Alert severity="info" sx={{ my: 2, backgroundColor: "#0F172A", color: "#94A3B8", border: "1px solid #334155" }}>
                Esta ferramenta gera o texto de divulgação com IA e organiza seus grupos — a publicação em grupos de WhatsApp/Facebook é feita por você, copiando e colando o texto. Não existe API pública que permita postar automaticamente em grupos de terceiros; por isso cadastre aqui os grupos dos quais você já participa.
            </Alert>

            {error && <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError("")}>{error}</Alert>}

            <Stepper activeStep={content ? 1 : 0} sx={{ mb: 3 }}>
                <Step><StepLabel>1. Gere seu texto com IA</StepLabel></Step>
                <Step><StepLabel>2. Escolha o grupo e copie</StepLabel></Step>
                <Step><StepLabel>3. Cole e publique</StepLabel></Step>
            </Stepper>

            {loading ? (
                <Box sx={{ display: "flex", justifyContent: "center", pt: 6 }}><CircularProgress sx={{ color: "#F97316" }} /></Box>
            ) : (
                <>
                    <Card sx={{ backgroundColor: "#0F172A", border: "1px solid #334155", mb: 3 }}>
                        <CardContent>
                            <Typography variant="subtitle1" color="#F8FAFC" fontWeight={600} sx={{ mb: 2 }}>
                                Passo 1 — Gere o texto
                            </Typography>
                            <Grid container spacing={2}>
                                <Grid item xs={12} sm={5}>
                                    <TextField
                                        select fullWidth label="Produto" value={productId}
                                        onChange={(e) => setProductId(e.target.value === "" ? "" : Number(e.target.value))}
                                        InputLabelProps={{ sx: { color: "#94A3B8" } }} InputProps={{ sx: { color: "#F8FAFC" } }}
                                    >
                                        {products.map((p) => (
                                            <MenuItem key={p.id} value={p.id}>{p.name}</MenuItem>
                                        ))}
                                    </TextField>
                                </Grid>
                                <Grid item xs={12} sm={4}>
                                    <TextField
                                        select fullWidth label="Tom do texto" value={tone}
                                        onChange={(e) => setTone(e.target.value)}
                                        InputLabelProps={{ sx: { color: "#94A3B8" } }} InputProps={{ sx: { color: "#F8FAFC" } }}
                                    >
                                        {TONES.map((t) => (
                                            <MenuItem key={t.value} value={t.value}>{t.label}</MenuItem>
                                        ))}
                                    </TextField>
                                </Grid>
                                <Grid item xs={12} sm={3} sx={{ display: "flex", alignItems: "center" }}>
                                    <Button
                                        fullWidth variant="contained" startIcon={<AutoAwesomeIcon />}
                                        onClick={handleGenerate} disabled={!productId || generating}
                                        sx={{ backgroundColor: "#F97316" }}
                                    >
                                        {generating ? "Gerando..." : "Gerar texto com IA"}
                                    </Button>
                                </Grid>
                            </Grid>

                            {content && (
                                <Box sx={{ mt: 3, p: 2, backgroundColor: "#1E293B", borderRadius: 1 }}>
                                    <Typography variant="body2" color="#F8FAFC" sx={{ whiteSpace: "pre-wrap", mb: 1 }}>
                                        {fullText()}
                                    </Typography>
                                    <Button size="small" startIcon={<ContentCopyIcon />} onClick={handleCopy} sx={{ color: "#10B981" }}>
                                        Copiar texto
                                    </Button>
                                </Box>
                            )}
                        </CardContent>
                    </Card>

                    <Typography variant="subtitle1" color="#F8FAFC" fontWeight={600} sx={{ mb: 1 }}>
                        Passo 2 — Escolha o grupo
                    </Typography>

                    <Box sx={{ display: "flex", gap: 1, mb: 2, flexWrap: "wrap" }}>
                        <TextField
                            size="small" placeholder="Buscar grupo por nome ou categoria"
                            value={search} onChange={(e) => setSearch(e.target.value)}
                            InputProps={{
                                sx: { color: "#F8FAFC" },
                                startAdornment: <InputAdornment position="start"><SearchIcon sx={{ color: "#94A3B8" }} /></InputAdornment>,
                            }}
                            sx={{ minWidth: 260 }}
                        />
                        {PLATFORM_FILTERS.map((f) => (
                            <Chip
                                key={f.value} label={f.label} clickable
                                onClick={() => setPlatformFilter(f.value)}
                                sx={{
                                    backgroundColor: platformFilter === f.value ? "#F97316" : "#1E293B",
                                    color: platformFilter === f.value ? "#0F172A" : "#94A3B8",
                                }}
                            />
                        ))}
                    </Box>

                    {filteredGroups.length === 0 ? (
                        <Typography color="#94A3B8">
                            Nenhum grupo cadastrado ainda. Clique em "Cadastrar Grupo" e adicione os grupos de WhatsApp/Facebook dos quais você participa.
                        </Typography>
                    ) : (
                        <Grid container spacing={2}>
                            {filteredGroups.map((g) => (
                                <Grid item xs={12} sm={6} md={4} key={g.id}>
                                    <Card sx={{ backgroundColor: "#0F172A", border: "1px solid #334155", height: "100%" }}>
                                        <CardContent>
                                            <Box sx={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start" }}>
                                                <Box sx={{ display: "flex", alignItems: "center", gap: 0.5 }}>
                                                    {g.platform === "whatsapp" ? (
                                                        <WhatsAppIcon sx={{ fontSize: 18, color: "#25D366" }} />
                                                    ) : (
                                                        <FacebookIcon sx={{ fontSize: 18, color: "#1877F2" }} />
                                                    )}
                                                    <Typography variant="body1" color="#F8FAFC" fontWeight={600}>{g.name}</Typography>
                                                </Box>
                                                <Box sx={{ display: "flex", gap: 0.5 }}>
                                                    <IconButton size="small" onClick={() => openEditDialog(g)} sx={{ color: "#94A3B8" }}>
                                                        <EditIcon fontSize="small" />
                                                    </IconButton>
                                                    <IconButton size="small" onClick={() => handleDeleteGroup(g.id)} sx={{ color: "#EF4444" }}>
                                                        <DeleteIcon fontSize="small" />
                                                    </IconButton>
                                                </Box>
                                            </Box>
                                            <Chip label={g.category} size="small" sx={{ mt: 1, height: 20, fontSize: 10, backgroundColor: "#1E293B", color: "#94A3B8" }} />
                                            {g.best_time && (
                                                <Box sx={{ display: "flex", alignItems: "center", gap: 0.5, mt: 1 }}>
                                                    <AccessTimeIcon sx={{ fontSize: 14, color: "#64748B" }} />
                                                    <Typography variant="caption" color="#64748B">Melhor horário: {g.best_time}</Typography>
                                                </Box>
                                            )}
                                            <Box sx={{ display: "flex", gap: 1, mt: 2 }}>
                                                <Button
                                                    fullWidth size="small" startIcon={<ContentCopyIcon />}
                                                    disabled={!content}
                                                    onClick={handleCopy}
                                                    sx={{ color: "#10B981", borderColor: "#10B981" }}
                                                    variant="outlined"
                                                >
                                                    Copiar
                                                </Button>
                                                <Button
                                                    fullWidth size="small" startIcon={<OpenInNewIcon />}
                                                    disabled={!content}
                                                    onClick={() => handlePublish(g)}
                                                    sx={{ backgroundColor: "#F97316" }}
                                                    variant="contained"
                                                >
                                                    Publicar
                                                </Button>
                                            </Box>
                                        </CardContent>
                                    </Card>
                                </Grid>
                            ))}
                        </Grid>
                    )}
                </>
            )}

            <Dialog open={dialogOpen} onClose={() => { setDialogOpen(false); setEditingId(null); }} maxWidth="sm" fullWidth PaperProps={{ sx: { backgroundColor: "#0F172A", color: "#F8FAFC" } }}>
                <DialogTitle>{editingId ? "Editar Grupo de Divulgação" : "Cadastrar Grupo de Divulgação"}</DialogTitle>
                <DialogContent sx={{ display: "flex", flexDirection: "column", gap: 2, pt: "8px !important" }}>
                    <TextField label="Nome do grupo" value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} InputLabelProps={{ sx: { color: "#94A3B8" } }} InputProps={{ sx: { color: "#F8FAFC" } }} />
                    <TextField select label="Plataforma" value={form.platform} onChange={(e) => setForm({ ...form, platform: e.target.value })} InputLabelProps={{ sx: { color: "#94A3B8" } }} InputProps={{ sx: { color: "#F8FAFC" } }}>
                        <MenuItem value="whatsapp">WhatsApp</MenuItem>
                        <MenuItem value="facebook">Facebook</MenuItem>
                    </TextField>
                    <TextField label="Categoria" value={form.category} onChange={(e) => setForm({ ...form, category: e.target.value })} InputLabelProps={{ sx: { color: "#94A3B8" } }} InputProps={{ sx: { color: "#F8FAFC" } }} />
                    <TextField label="Link do grupo (opcional)" value={form.link} onChange={(e) => setForm({ ...form, link: e.target.value })} InputLabelProps={{ sx: { color: "#94A3B8" } }} InputProps={{ sx: { color: "#F8FAFC" } }} />
                    <TextField label="Melhor horário (ex: 19h-21h)" value={form.best_time} onChange={(e) => setForm({ ...form, best_time: e.target.value })} InputLabelProps={{ sx: { color: "#94A3B8" } }} InputProps={{ sx: { color: "#F8FAFC" } }} />
                    <TextField label="Nº de membros (opcional)" type="number" value={form.member_count} onChange={(e) => setForm({ ...form, member_count: e.target.value })} InputLabelProps={{ sx: { color: "#94A3B8" } }} InputProps={{ sx: { color: "#F8FAFC" } }} />
                </DialogContent>
                <DialogActions>
                    <Button onClick={() => { setDialogOpen(false); setEditingId(null); }} sx={{ color: "#94A3B8" }}>Cancelar</Button>
                    <Button onClick={handleSaveGroup} variant="contained" sx={{ backgroundColor: "#2563EB" }}>Salvar</Button>
                </DialogActions>
            </Dialog>

            <Snackbar open={!!toast} autoHideDuration={3000} onClose={() => setToast("")} message={toast} />
        </Box>
    );
}
