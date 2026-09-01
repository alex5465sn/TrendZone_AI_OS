import { useEffect, useState } from "react";

import {
    Box,
    Typography,
    Grid,
    Card,
    CardContent,
    CircularProgress,
    Alert,
    Chip,
    Avatar,
} from "@mui/material";

import TrendingUpIcon from "@mui/icons-material/TrendingUp";
import StarIcon from "@mui/icons-material/Star";
import AttachMoneyIcon from "@mui/icons-material/AttachMoney";

import { searchShopeeProducts, type ShopeeProductNode } from "../../services/marketplaceService";

function calculateScore(product: ShopeeProductNode): number {

    const rating = Number(product.ratingStar) || 0;
    const sales = product.sales || 0;
    const commission = Number(product.commissionRate) || 0;

    const salesScore = Math.min(sales / 100, 30);
    const ratingScore = (rating / 5) * 30;
    const commissionScore = commission * 100 * 2;

    return Math.min(Math.round(salesScore + ratingScore + commissionScore), 100);

}

export default function Analytics() {

    const [products, setProducts] = useState<ShopeeProductNode[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    useEffect(() => {

        async function loadData() {

            try {

                const data = await searchShopeeProducts({
                    keyword: "tendencia",
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
                    .slice(0, 20);

                setProducts(scored as ShopeeProductNode[]);

            } catch (err) {

                console.error(err);
                setError("Erro ao carregar análises.");

            } finally {

                setLoading(false);

            }

        }

        loadData();

    }, []);

    if (loading) {

        return (
            <Box display="flex" justifyContent="center" alignItems="center" minHeight="60vh">
                <CircularProgress />
            </Box>
        );

    }

    if (error) {

        return (
            <Alert severity="error" sx={{ m: 2 }}>
                {error}
            </Alert>
        );

    }

    const avgCommission = products.length
        ? (products.reduce((sum, p) => sum + Number(p.commissionRate), 0) / products.length * 100).toFixed(1)
        : "0";

    const avgRating = products.length
        ? (products.reduce((sum, p) => sum + Number(p.ratingStar), 0) / products.length).toFixed(1)
        : "0";

    const totalSales = products.reduce((sum, p) => sum + p.sales, 0);

    return (

        <Box>

            <Typography
                variant="h4"
                fontWeight="bold"
                color="#F8FAFC"
                mb={1}
            >
                Análises
            </Typography>

            <Typography
                variant="body1"
                color="#94A3B8"
                mb={4}
            >
                Visão geral das oportunidades encontradas na Shopee.
            </Typography>

            <Grid container spacing={3} mb={4}>

                <Grid item xs={12} md={4}>
                    <Card sx={{ backgroundColor: "#111827", borderRadius: 3, border: "1px solid #1E293B" }}>
                        <CardContent>
                            <Typography color="#94A3B8" mb={1}>
                                <AttachMoneyIcon sx={{ verticalAlign: "middle", mr: 1 }} />
                                Comissão Média
                            </Typography>
                            <Typography variant="h4" fontWeight="bold" color="#F8FAFC">
                                {avgCommission}%
                            </Typography>
                        </CardContent>
                    </Card>
                </Grid>

                <Grid item xs={12} md={4}>
                    <Card sx={{ backgroundColor: "#111827", borderRadius: 3, border: "1px solid #1E293B" }}>
                        <CardContent>
                            <Typography color="#94A3B8" mb={1}>
                                <StarIcon sx={{ verticalAlign: "middle", mr: 1 }} />
                                Avaliação Média
                            </Typography>
                            <Typography variant="h4" fontWeight="bold" color="#F8FAFC">
                                {avgRating} ★
                            </Typography>
                        </CardContent>
                    </Card>
                </Grid>

                <Grid item xs={12} md={4}>
                    <Card sx={{ backgroundColor: "#111827", borderRadius: 3, border: "1px solid #1E293B" }}>
                        <CardContent>
                            <Typography color="#94A3B8" mb={1}>
                                <TrendingUpIcon sx={{ verticalAlign: "middle", mr: 1 }} />
                                Total de Vendas
                            </Typography>
                            <Typography variant="h4" fontWeight="bold" color="#F8FAFC">
                                {totalSales.toLocaleString("pt-BR")}
                            </Typography>
                        </CardContent>
                    </Card>
                </Grid>

            </Grid>

            <Grid container spacing={3}>

                {products.slice(0, 6).map((product: ShopeeProductNode & { _score?: number }) => {

                    const score = product._score || calculateScore(product);
                    let color: "success" | "warning" | "info" | "error" = "error";

                    if (score >= 80) { color = "success"; }
                    else if (score >= 60) { color = "warning"; }
                    else if (score >= 40) { color = "info"; }

                    return (

                        <Grid item xs={12} md={6} key={product.itemId}>

                            <Card sx={{ backgroundColor: "#111827", borderRadius: 3, border: "1px solid #1E293B" }}>

                                <CardContent>

                                    <Box sx={{ display: "flex", gap: 2, alignItems: "center" }}>

                                        <Avatar
                                            src={product.imageUrl}
                                            alt={product.productName}
                                            variant="rounded"
                                            sx={{ width: 64, height: 64 }}
                                        />

                                        <Box flex={1}>
                                            <Typography color="#F8FAFC" fontWeight="bold" sx={{ mb: 0.5 }}>
                                                {product.productName}
                                            </Typography>
                                            <Box sx={{ display: "flex", gap: 1, flexWrap: "wrap" }}>
                                                <Chip label={`Score ${score}`} size="small" color={color} />
                                                <Chip label={`R$ ${product.price}`} size="small" sx={{ backgroundColor: "#1E293B", color: "#F8FAFC" }} />
                                                <Chip label={`${(Number(product.commissionRate) * 100).toFixed(1)}%`} size="small" sx={{ backgroundColor: "#10B98133", color: "#10B981" }} />
                                                <Chip label={`${product.sales} vendas`} size="small" sx={{ backgroundColor: "#1E293B", color: "#94A3B8" }} />
                                            </Box>
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
