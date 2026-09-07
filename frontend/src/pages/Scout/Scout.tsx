import { useState, useEffect } from "react";

import {
    Box,
    Typography,
    TextField,
    Button,
    Grid,
    CircularProgress,
    Alert,
    Card,
    CardContent,
    Chip,
    Avatar,
    ToggleButton,
    ToggleButtonGroup,
} from "@mui/material";

import SmartToyIcon from "@mui/icons-material/SmartToy";
import TrendingUpIcon from "@mui/icons-material/TrendingUp";
import AttachMoneyIcon from "@mui/icons-material/AttachMoney";
import AddIcon from "@mui/icons-material/Add";
import CampaignIcon from "@mui/icons-material/Campaign";

import FacebookIcon from "@mui/icons-material/Facebook";

import { searchShopeeProducts, type ShopeeProductNode } from "../../services/marketplaceService";
import { createProduct } from "../../services/productService";
import { CATEGORIES, getKeywordsForCategories } from "../../constants/categories";
import { generateFacebookPost } from "../../utils/postGenerator";
import { getFacebookStatus, postToFacebook } from "../../services/facebookService";

function calculateScore(product: ShopeeProductNode): number {

    const rating = Number(product.ratingStar) || 0;
    const sales = product.sales || 0;
    const commission = Number(product.commissionRate) || 0;
    const discount = Number(product.priceDiscountRate) || 0;

    // Sinais de "produto campeão com venda rápida":
    // vendas acumuladas + avaliação + comissão + desconto ativo (indica campanha/promoção em andamento)
    const salesScore = Math.min(sales / 80, 35);
    const ratingScore = (rating / 5) * 25;
    const commissionScore = Math.min(commission * 100 * 1.5, 20);
    const velocityScore = Math.min(discount / 5, 20);

    return Math.min(Math.round(salesScore + ratingScore + commissionScore + velocityScore), 100);

}

function getDecision(score: number) {

    if (score >= 80) return { label: "PROMOVER", color: "success" as const };
    if (score >= 60) return { label: "TESTAR", color: "warning" as const };
    if (score >= 40) return { label: "OBSERVAR", color: "info" as const };
    return { label: "DESCARTAR", color: "error" as const };

}

export default function Scout() {

    const [keyword, setKeyword] = useState("");
    const [products, setProducts] = useState<ShopeeProductNode[]>([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");
    const [searched, setSearched] = useState(false);
    const [addingProduct, setAddingProduct] = useState<number | null>(null);
    const [selectedCategories, setSelectedCategories] = useState<string[]>(() => {
        try {
            const raw = localStorage.getItem("trendzone_settings");
            if (raw) return JSON.parse(raw).favoriteCategories || [];
        } catch {
            // ignora
        }
        return [];
    });
    const [postProductId, setPostProductId] = useState<number | null>(null);
    const [postText, setPostText] = useState("");
    const [postProduct, setPostProduct] = useState<ShopeeProductNode | null>(null);
    const [fbConfigured, setFbConfigured] = useState(false);
    const [posting, setPosting] = useState(false);
    const [postedIds, setPostedIds] = useState<number[]>(() => {
        try {
            const raw = localStorage.getItem("trendzone_fb_posted");
            if (raw) return JSON.parse(raw);
        } catch {
            // ignora
        }
        return [];
    });

    useEffect(() => {
        getFacebookStatus()
            .then((s) => setFbConfigured(s.configured))
            .catch(() => setFbConfigured(false));
    }, []);

    function markAsPosted(itemId: number) {
        setPostedIds((prev) => {
            const next = [...prev, itemId];
            localStorage.setItem("trendzone_fb_posted", JSON.stringify(next));
            return next;
        });
    }

    async function handleSearch() {

        if (!keyword.trim()) return;

        try {

            setLoading(true);
            setError("");
            setSearched(true);

            const data = await searchShopeeProducts({
                keyword,
                page: 1,
                limit: 50,
                sortType: 2,
            });

            const scored = (data.nodes || [])
                .map((product) => ({
                    ...product,
                    _score: calculateScore(product),
                }))
                .sort((a, b) => b._score - a._score)
                .slice(0, 10);

            setProducts(scored as ShopeeProductNode[]);

        } catch (err) {

            console.error(err);
            setError("Erro ao buscar produtos na Shopee.");

        } finally {

            setLoading(false);

        }

    }

    async function handleFindChampions() {

        const keywords = getKeywordsForCategories(selectedCategories);

        try {

            setLoading(true);
            setError("");
            setSearched(true);

            const results = await Promise.allSettled(
                keywords.map((kw) =>
                    searchShopeeProducts({ keyword: kw, page: 1, limit: 20, sortType: 2 })
                )
            );

            const allNodes: ShopeeProductNode[] = [];
            const seen = new Set<number>();

            for (const r of results) {
                if (r.status === "fulfilled") {
                    for (const node of r.value.nodes || []) {
                        if (!seen.has(node.itemId)) {
                            seen.add(node.itemId);
                            allNodes.push(node);
                        }
                    }
                }
            }

            const scored = allNodes
                .map((product) => ({ ...product, _score: calculateScore(product) }))
                .sort((a, b) => b._score - a._score)
                .slice(0, 20);

            setProducts(scored as ShopeeProductNode[]);

            if (scored.length === 0) {
                setError("Nenhum produto campeão encontrado agora. Tente novamente em alguns minutos.");
            }

        } catch (err) {

            console.error(err);
            setError("Erro ao buscar produtos campeões.");

        } finally {

            setLoading(false);

        }

    }

    function handleGeneratePost(product: ShopeeProductNode) {
        const text = generateFacebookPost({
            productName: product.productName,
            price: product.price,
            priceDiscountRate: product.priceDiscountRate,
            offerLink: product.offerLink,
            commissionRate: product.commissionRate,
        });
        setPostText(text);
        setPostProductId(product.itemId);
        setPostProduct(product);
    }

    async function handleCopyPost() {
        try {
            await navigator.clipboard.writeText(postText);
            alert("Texto copiado! Cole na sua página do Facebook.");
        } catch {
            alert("Não foi possível copiar automaticamente. Selecione e copie o texto manualmente.");
        }
    }

    async function handlePostToFacebook() {

        if (!postProduct) return;

        if (postedIds.includes(postProduct.itemId)) {
            if (!window.confirm("Este produto já foi postado no Facebook antes. Postar de novo mesmo assim?")) {
                return;
            }
        }

        try {

            setPosting(true);

            await postToFacebook({
                message: postText,
                link: postProduct.offerLink,
                image_url: postProduct.imageUrl,
            });

            markAsPosted(postProduct.itemId);
            alert("✓ Publicado na página do Facebook com sucesso!");

        } catch (err: any) {

            console.error(err);
            alert(err.response?.data?.message || "✗ Erro ao publicar no Facebook.");

        } finally {

            setPosting(false);

        }

    }

    async function handleAddProduct(product: ShopeeProductNode) {

        try {

            setAddingProduct(product.itemId);

            await createProduct({
                item_id: product.itemId,
                shop_id: product.shopId,
                name: product.productName,
                price: Number(product.price),
                commission: Number(product.commissionRate) * 100,
                image: product.imageUrl,
                offer_link: product.offerLink,
            });

            alert(`✓ Produto "${product.productName}" adicionado ao tracker!`);

        } catch (err) {

            console.error(err);
            alert("✗ Erro ao adicionar produto ao tracker.");

        } finally {

            setAddingProduct(null);

        }

    }

    return (

        <Box>

            <Typography
                variant="h4"
                fontWeight="bold"
                color="#F8FAFC"
                mb={1}
            >
                Scout IA
            </Typography>

            <Typography
                variant="body1"
                color="#94A3B8"
                mb={4}
            >
                Análise inteligente de produtos da Shopee com scoring automático.
            </Typography>

            <Box
                sx={{
                    display: "flex",
                    gap: 2,
                    mb: 4,
                }}
            >

                <TextField
                    value={keyword}
                    onChange={(e) => setKeyword(e.target.value)}
                    onKeyDown={(e) => e.key === "Enter" && handleSearch()}
                    placeholder="Ex: fone de ouvido, smartwatch, bolsas..."
                    sx={{
                        flex: 1,
                        backgroundColor: "#111827",
                        borderRadius: 2,
                        input: { color: "#F8FAFC" },
                    }}
                />

                <Button
                    variant="contained"
                    startIcon={<SmartToyIcon />}
                    onClick={handleSearch}
                    disabled={loading}
                    sx={{
                        backgroundColor: "#8B5CF6",
                        textTransform: "none",
                        borderRadius: 2,
                        px: 4,
                    }}
                >
                    {loading ? <CircularProgress size={20} color="inherit" /> : "Analisar"}
                </Button>

            </Box>

            <Box sx={{ mb: 2 }}>

                <Typography color="#94A3B8" fontSize="0.85rem" mb={1}>
                    Ou deixe o agente IA varrer categorias inteiras em busca de produtos campeões (deixe nenhuma marcada para buscar em todas):
                </Typography>

                <ToggleButtonGroup
                    value={selectedCategories}
                    onChange={(_, value) => setSelectedCategories(value)}
                    sx={{ flexWrap: "wrap", gap: 1, mb: 2 }}
                >
                    {CATEGORIES.map((cat) => (
                        <ToggleButton
                            key={cat.id}
                            value={cat.id}
                            sx={{
                                color: "#94A3B8",
                                borderColor: "#1E293B",
                                textTransform: "none",
                                "&.Mui-selected": {
                                    backgroundColor: "#8B5CF633",
                                    color: "#8B5CF6",
                                },
                            }}
                        >
                            {cat.label}
                        </ToggleButton>
                    ))}
                </ToggleButtonGroup>

                <Box>
                    <Button
                        variant="contained"
                        startIcon={<TrendingUpIcon />}
                        onClick={handleFindChampions}
                        disabled={loading}
                        sx={{
                            backgroundColor: "#10B981",
                            textTransform: "none",
                            borderRadius: 2,
                            px: 4,
                        }}
                    >
                        {loading ? <CircularProgress size={20} color="inherit" /> : "Encontrar Produtos Campeões"}
                    </Button>
                </Box>

            </Box>

            {postProductId !== null && (
                <Alert
                    severity="info"
                    sx={{ mb: 3, whiteSpace: "pre-wrap" }}
                    onClose={() => setPostProductId(null)}
                    action={
                        <Box sx={{ display: "flex", gap: 1 }}>
                            <Button color="inherit" size="small" onClick={handleCopyPost}>
                                Copiar
                            </Button>
                            <Button
                                color="inherit"
                                size="small"
                                startIcon={<FacebookIcon />}
                                onClick={handlePostToFacebook}
                                disabled={!fbConfigured || posting}
                            >
                                {posting
                                    ? "Publicando..."
                                    : postProduct && postedIds.includes(postProduct.itemId)
                                    ? "Postar de novo"
                                    : "Postar no Facebook"}
                            </Button>
                        </Box>
                    }
                >
                    {postText}
                    {!fbConfigured && (
                        <Typography variant="caption" display="block" mt={1} color="#94A3B8">
                            Postagem automática indisponível: configure FACEBOOK_PAGE_ID e FACEBOOK_PAGE_TOKEN no .env do servidor.
                        </Typography>
                    )}
                </Alert>
            )}

            {error && (
                <Alert severity="error" sx={{ mb: 3 }}>
                    {error}
                </Alert>
            )}

            {searched && products.length === 0 && !loading && !error && (
                <Alert severity="info" sx={{ mb: 3 }}>
                    Nenhum produto encontrado. Tente outra palavra-chave.
                </Alert>
            )}

            <Grid container spacing={3}>

                {products.map((product: ShopeeProductNode & { _score?: number }) => {

                    const score = product._score || calculateScore(product);
                    const decision = getDecision(score);

                    return (

                        <Grid item xs={12} md={6} key={product.itemId}>

                            <Card
                                sx={{
                                    backgroundColor: "#111827",
                                    border: "1px solid #1E293B",
                                    borderRadius: 3,
                                    height: "100%",
                                }}
                            >

                                <CardContent>

                                    <Box
                                        sx={{
                                            display: "flex",
                                            gap: 2,
                                            mb: 2,
                                        }}
                                    >

                                        <Avatar
                                            src={product.imageUrl}
                                            alt={product.productName}
                                            variant="rounded"
                                            sx={{ width: 80, height: 80 }}
                                        />

                                        <Box flex={1}>

                                            <Typography
                                                variant="h6"
                                                fontWeight="bold"
                                                color="#F8FAFC"
                                                sx={{
                                                    fontSize: "1rem",
                                                    lineHeight: 1.3,
                                                    mb: 1,
                                                }}
                                            >
                                                {product.productName}
                                            </Typography>

                                            <Chip
                                                label={decision.label}
                                                color={decision.color}
                                                size="small"
                                                sx={{ fontWeight: 600 }}
                                            />

                                        </Box>

                                    </Box>

                                    <Grid container spacing={2} mb={2}>

                                        <Grid item xs={4}>
                                            <Box textAlign="center">
                                                <Typography color="#94A3B8" fontSize="0.75rem">
                                                    SCORE IA
                                                </Typography>
                                                <Typography
                                                    color="#F8FAFC"
                                                    fontWeight="bold"
                                                    variant="h5"
                                                >
                                                    {score}
                                                </Typography>
                                            </Box>
                                        </Grid>

                                        <Grid item xs={4}>
                                            <Box textAlign="center">
                                                <Typography color="#94A3B8" fontSize="0.75rem">
                                                    <AttachMoneyIcon sx={{ fontSize: 14, verticalAlign: "middle" }} />
                                                    COMISSÃO
                                                </Typography>
                                                <Typography
                                                    color="#F8FAFC"
                                                    fontWeight="bold"
                                                    variant="h5"
                                                >
                                                    {(Number(product.commissionRate) * 100).toFixed(1)}%
                                                </Typography>
                                            </Box>
                                        </Grid>

                                        <Grid item xs={4}>
                                            <Box textAlign="center">
                                                <Typography color="#94A3B8" fontSize="0.75rem">
                                                    <TrendingUpIcon sx={{ fontSize: 14, verticalAlign: "middle" }} />
                                                    VENDAS
                                                </Typography>
                                                <Typography
                                                    color="#F8FAFC"
                                                    fontWeight="bold"
                                                    variant="h5"
                                                >
                                                    {product.sales}
                                                </Typography>
                                            </Box>
                                        </Grid>

                                    </Grid>

                                    <Box
                                        sx={{
                                            display: "flex",
                                            justifyContent: "space-between",
                                            alignItems: "center",
                                            gap: 1,
                                        }}
                                    >

                                        <Typography
                                            color="#F8FAFC"
                                            fontWeight="bold"
                                            variant="h6"
                                        >
                                            R$ {product.price}
                                        </Typography>

                                        <Box sx={{ display: "flex", gap: 1 }}>

                                            <Button
                                                href={product.offerLink}
                                                target="_blank"
                                                rel="noopener noreferrer"
                                                size="small"
                                                sx={{
                                                    color: "#38BDF8",
                                                    textTransform: "none",
                                                }}
                                            >
                                                Ver
                                            </Button>

                                            <Button
                                                startIcon={<CampaignIcon />}
                                                onClick={() => handleGeneratePost(product)}
                                                size="small"
                                                sx={{
                                                    backgroundColor: "#38BDF833",
                                                    color: "#38BDF8",
                                                    textTransform: "none",
                                                    "&:hover": {
                                                        backgroundColor: "#38BDF855",
                                                    },
                                                }}
                                            >
                                                Gerar Post
                                            </Button>

                                            <Button
                                                startIcon={<AddIcon />}
                                                onClick={() => handleAddProduct(product)}
                                                disabled={addingProduct === product.itemId}
                                                size="small"
                                                sx={{
                                                    backgroundColor: "#10B98133",
                                                    color: "#10B981",
                                                    textTransform: "none",
                                                    "&:hover": {
                                                        backgroundColor: "#10B98155",
                                                    },
                                                }}
                                            >
                                                {addingProduct === product.itemId ? "..." : "Adicionar"}
                                            </Button>

                                        </Box>

                                    </Box>

                                </CardContent>

                            </Card>

                        </Grid>

                    );

                })}

            </Grid>

        </Box>

    );

}
