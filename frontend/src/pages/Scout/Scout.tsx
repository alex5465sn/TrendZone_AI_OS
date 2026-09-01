import { useState } from "react";

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
} from "@mui/material";

import SmartToyIcon from "@mui/icons-material/SmartToy";
import TrendingUpIcon from "@mui/icons-material/TrendingUp";
import AttachMoneyIcon from "@mui/icons-material/AttachMoney";
import AddIcon from "@mui/icons-material/Add";

import { searchShopeeProducts, type ShopeeProductNode } from "../../services/marketplaceService";
import { createProduct } from "../../services/productService";

function calculateScore(product: ShopeeProductNode): number {

    const rating = Number(product.ratingStar) || 0;
    const sales = product.sales || 0;
    const commission = Number(product.commissionRate) || 0;

    const salesScore = Math.min(sales / 100, 30);
    const ratingScore = (rating / 5) * 30;
    const commissionScore = commission * 100 * 2;

    return Math.min(Math.round(salesScore + ratingScore + commissionScore), 100);

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
