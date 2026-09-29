import { useEffect, useState, useCallback } from "react";

import {
    Box,
    Typography,
    CircularProgress,
    Alert,
    Button,
    TextField,
    Grid,
    Chip,
    Dialog,
    DialogTitle,
    DialogContent,
    DialogActions,
    IconButton,
} from "@mui/material";

import SearchIcon from "@mui/icons-material/Search";
import TrendingUpIcon from "@mui/icons-material/TrendingUp";
import AttachMoneyIcon from "@mui/icons-material/AttachMoney";
import StarIcon from "@mui/icons-material/Star";
import CampaignIcon from "@mui/icons-material/Campaign";
import ContentCopyIcon from "@mui/icons-material/ContentCopy";
import WhatsAppIcon from "@mui/icons-material/WhatsApp";
import FacebookIcon from "@mui/icons-material/Facebook";
import OpenInNewIcon from "@mui/icons-material/OpenInNew";
import CloseIcon from "@mui/icons-material/Close";

import ShopeeProductTable from "../../components/products/ShopeeProductTable";
import {
    searchShopeeProducts,
    promoteProduct,
    type ShopeeProductNode,
    type PromoteResult,
} from "../../services/marketplaceService";
import { createProduct } from "../../services/productService";
import { CATEGORIES } from "../../constants/categories";

export default function Products() {

    const [products, setProducts] = useState<ShopeeProductNode[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");
    const [keyword, setKeyword] = useState("tendencia");
    const [activeCategory, setActiveCategory] = useState<string | null>(null);
    const [selectedIds, setSelectedIds] = useState<Set<number>>(new Set());
    const [promoting, setPromoting] = useState(false);
    const [promoteResults, setPromoteResults] = useState<
        { product: ShopeeProductNode; result: PromoteResult }[]
    >([]);
    const [promoteDialogOpen, setPromoteDialogOpen] = useState(false);
    const [promoteError, setPromoteError] = useState("");

    const loadProducts = useCallback(async (search: string) => {

        try {

            setLoading(true);
            setError("");

            const data = await searchShopeeProducts({
                keyword: search,
                page: 1,
                limit: 20,
                sortType: 1,
            });

            setProducts(data.nodes || []);

        } catch (err) {

            console.error(err);
            setError("Erro ao buscar produtos na Shopee.");

        } finally {

            setLoading(false);

        }

    }, []);

    useEffect(() => {

        loadProducts(keyword);

    }, [keyword, loadProducts]);

    function handleSearch() {

        loadProducts(keyword);

    }

    function handleCategory(categoryId: string, categoryKeywords: string[]) {

        setActiveCategory(categoryId);
        setKeyword(categoryKeywords[0] || categoryId);

    }

    async function handleAdd(product: ShopeeProductNode) {

        try {

            await createProduct({
                item_id: product.itemId,
                shop_id: product.shopId,
                category: activeCategory || "geral",
                name: product.productName,
                price: Number(product.price),
                commission: Number(product.commissionRate) * 100,
                image: product.imageUrl,
                offer_link: product.offerLink,
                rating: Number(product.ratingStar) || 0,
                sales: Number(product.sales) || 0,
            });

            alert(`✓ Produto "${product.productName}" adicionado ao tracker!`);

        } catch (err: any) {

            if (err?.response?.status === 409) {
                alert(`Produto "${product.productName}" já está rastreado.`);
            } else {
                alert("Erro ao adicionar produto ao tracker.");
            }

        }

    }

    function toggleSelect(itemId: number) {

        setSelectedIds((prev) => {
            const next = new Set(prev);
            if (next.has(itemId)) {
                next.delete(itemId);
            } else {
                next.add(itemId);
            }
            return next;
        });

    }

    function toggleSelectAll() {

        setSelectedIds((prev) =>
            prev.size === products.length
                ? new Set()
                : new Set(products.map((p) => p.itemId))
        );

    }

    async function promoteOne(product: ShopeeProductNode) {

        const result = await promoteProduct({
            item_id: product.itemId,
            product_name: product.productName,
            price: Number(product.price) || 0,
            commission_rate: Number(product.commissionRate) || 0,
            rating_star: Number(product.ratingStar) || 0,
            sales: Number(product.sales) || 0,
            offer_link: product.offerLink,
        });

        return { product, result };

    }

    async function handlePromote(product: ShopeeProductNode) {

        setPromoteError("");
        setPromoting(true);
        setPromoteDialogOpen(true);

        try {
            const entry = await promoteOne(product);
            setPromoteResults([entry]);
        } catch (err) {
            console.error(err);
            setPromoteError("Erro ao gerar conteúdo de divulgação para o produto.");
            setPromoteResults([]);
        } finally {
            setPromoting(false);
        }

    }

    async function handlePromoteSelected() {

        const selected = products.filter((p) => selectedIds.has(p.itemId));
        if (selected.length === 0) return;

        setPromoteError("");
        setPromoting(true);
        setPromoteDialogOpen(true);
        setPromoteResults([]);

        try {
            const entries = await Promise.all(selected.map((product) => promoteOne(product)));
            setPromoteResults(entries);
        } catch (err) {
            console.error(err);
            setPromoteError("Erro ao gerar conteúdo de divulgação para um ou mais produtos.");
        } finally {
            setPromoting(false);
        }

    }

    function copyText(text: string) {

        navigator.clipboard.writeText(text).catch(() => undefined);

    }

    if (loading) {

        return (
            <Box display="flex" justifyContent="center" alignItems="center" minHeight="60vh">
                <CircularProgress />
            </Box>
        );

    }

    return (

        <Box>

            <Typography
                variant="h4"
                fontWeight="bold"
                color="#F8FAFC"
                mb={1}
            >
                Produtos Shopee
            </Typography>

            <Typography
                variant="body1"
                color="#94A3B8"
                mb={4}
            >
                Busque produtos em tempo real e identifique oportunidades de afiliados.
            </Typography>

            <Box
                sx={{
                    display: "flex",
                    gap: 2,
                    mb: 3,
                    flexWrap: "wrap",
                }}
            >

                <TextField
                    value={keyword}
                    onChange={(e) => setKeyword(e.target.value)}
                    onKeyDown={(e) => e.key === "Enter" && handleSearch()}
                    placeholder="Ex: fone de ouvido, smartwatch, bolsas..."
                    sx={{
                        flex: 1,
                        minWidth: 300,
                        backgroundColor: "#111827",
                        borderRadius: 2,
                        input: { color: "#F8FAFC" },
                    }}
                />

                <Button
                    variant="contained"
                    startIcon={<SearchIcon />}
                    onClick={handleSearch}
                    sx={{
                        backgroundColor: "#2563EB",
                        textTransform: "none",
                        borderRadius: 2,
                        px: 4,
                    }}
                >
                    Buscar
                </Button>

            </Box>

            <Box
                sx={{
                    display: "flex",
                    gap: 1,
                    mb: 4,
                    flexWrap: "wrap",
                }}
            >

                {CATEGORIES.filter((category) => category.keywords.length > 0).map((category) => (

                    <Chip
                        key={category.id}
                        label={category.label}
                        onClick={() => handleCategory(category.id, category.keywords)}
                        sx={{
                            backgroundColor: activeCategory === category.id ? "#2563EB" : "#1E293B",
                            color: "#F8FAFC",
                            fontWeight: 500,
                            cursor: "pointer",
                            "&:hover": {
                                backgroundColor: "#2563EB",
                            },
                        }}
                    />

                ))}

            </Box>

            <Grid container spacing={3} mb={4}>

                <Grid item xs={12} md={4}>
                    <Box
                        sx={{
                            p: 3,
                            borderRadius: 3,
                            backgroundColor: "#111827",
                            border: "1px solid #1E293B",
                        }}
                    >
                        <Typography color="#94A3B8" mb={1}>
                            <TrendingUpIcon sx={{ verticalAlign: "middle", mr: 1 }} />
                            Produtos Encontrados
                        </Typography>
                        <Typography variant="h4" fontWeight="bold" color="#F8FAFC">
                            {products.length}
                        </Typography>
                    </Box>
                </Grid>

                <Grid item xs={12} md={4}>
                    <Box
                        sx={{
                            p: 3,
                            borderRadius: 3,
                            backgroundColor: "#111827",
                            border: "1px solid #1E293B",
                        }}
                    >
                        <Typography color="#94A3B8" mb={1}>
                            <AttachMoneyIcon sx={{ verticalAlign: "middle", mr: 1 }} />
                            Maior Comissão
                        </Typography>
                        <Typography variant="h4" fontWeight="bold" color="#F8FAFC">
                            {products.length > 0
                                ? `${Math.max(...products.map((p) => Number(p.commissionRate) * 100)).toFixed(1)}%`
                                : "-"}
                        </Typography>
                    </Box>
                </Grid>

                <Grid item xs={12} md={4}>
                    <Box
                        sx={{
                            p: 3,
                            borderRadius: 3,
                            backgroundColor: "#111827",
                            border: "1px solid #1E293B",
                        }}
                    >
                        <Typography color="#94A3B8" mb={1}>
                            <StarIcon sx={{ verticalAlign: "middle", mr: 1 }} />
                            Melhor Avaliação
                        </Typography>
                        <Typography variant="h4" fontWeight="bold" color="#F8FAFC">
                            {products.length > 0
                                ? Math.max(...products.map((p) => Number(p.ratingStar))).toFixed(1)
                                : "-"}
                        </Typography>
                    </Box>
                </Grid>

            </Grid>

            {error && (
                <Alert severity="error" sx={{ mb: 3 }}>
                    {error}
                </Alert>
            )}

            {selectedIds.size > 0 && (
                <Box
                    sx={{
                        display: "flex",
                        alignItems: "center",
                        gap: 2,
                        mb: 2,
                        p: 2,
                        borderRadius: 2,
                        backgroundColor: "#1E293B",
                    }}
                >
                    <Typography color="#F8FAFC">
                        {selectedIds.size} produto(s) selecionado(s)
                    </Typography>
                    <Button
                        variant="contained"
                        startIcon={<CampaignIcon />}
                        onClick={handlePromoteSelected}
                        sx={{ backgroundColor: "#10B981", textTransform: "none" }}
                    >
                        Divulgar selecionados
                    </Button>
                </Box>
            )}

            <ShopeeProductTable
                products={products}
                onAdd={handleAdd}
                onPromote={handlePromote}
                selectedIds={selectedIds}
                onToggleSelect={toggleSelect}
                onToggleSelectAll={toggleSelectAll}
            />

            <Dialog
                open={promoteDialogOpen}
                onClose={() => setPromoteDialogOpen(false)}
                maxWidth="sm"
                fullWidth
            >
                <DialogTitle sx={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                    Divulgar produto(s)
                    <IconButton onClick={() => setPromoteDialogOpen(false)}>
                        <CloseIcon />
                    </IconButton>
                </DialogTitle>
                <DialogContent dividers>
                    {promoting && (
                        <Box display="flex" justifyContent="center" py={4}>
                            <CircularProgress />
                        </Box>
                    )}

                    {promoteError && <Alert severity="error" sx={{ mb: 2 }}>{promoteError}</Alert>}

                    {!promoting && promoteResults.map(({ product, result }) => (
                        <Box
                            key={product.itemId}
                            sx={{ mb: 3, pb: 3, borderBottom: "1px solid #1E293B" }}
                        >
                            <Typography fontWeight="bold" mb={1}>
                                {product.productName}
                            </Typography>
                            <Typography variant="body2" sx={{ whiteSpace: "pre-line", mb: 2 }}>
                                {result.full_text}
                            </Typography>
                            <Box sx={{ display: "flex", gap: 1, flexWrap: "wrap" }}>
                                <Button
                                    size="small"
                                    startIcon={<ContentCopyIcon />}
                                    onClick={() => copyText(result.full_text)}
                                >
                                    Copiar texto
                                </Button>
                                <Button
                                    size="small"
                                    startIcon={<WhatsAppIcon />}
                                    href={result.whatsapp_share_url}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                >
                                    WhatsApp
                                </Button>
                                <Button
                                    size="small"
                                    startIcon={<FacebookIcon />}
                                    href={result.facebook_share_url}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                >
                                    Facebook
                                </Button>
                                <Button
                                    size="small"
                                    startIcon={<OpenInNewIcon />}
                                    href={result.tracking_url}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                >
                                    Link de rastreamento
                                </Button>
                            </Box>
                        </Box>
                    ))}
                </DialogContent>
                <DialogActions>
                    <Button onClick={() => setPromoteDialogOpen(false)}>Fechar</Button>
                </DialogActions>
            </Dialog>

        </Box>

    );

}
