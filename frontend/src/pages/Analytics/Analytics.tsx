import { useEffect, useState } from "react";

import {
    Box,
    Typography,
    Grid,
    Card,
    CardContent,
    CircularProgress,
    Alert,
} from "@mui/material";

import TrendingUpIcon from "@mui/icons-material/TrendingUp";
import StarIcon from "@mui/icons-material/Star";
import AttachMoneyIcon from "@mui/icons-material/AttachMoney";

import {
    BarChart,
    Bar,
    LineChart,
    Line,
    PieChart,
    Pie,
    Cell,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    Legend,
    ResponsiveContainer,
} from "recharts";

import {
    getProductsSummary,
    getProductsByScore,
    getProductsByCommission,
    getTopProducts,
    getCommissionSummary,
    getSalesByRating,
    type ProductSummary,
    type ScoreDistribution,
    type CommissionDistribution,
    type TopProduct,
    type CommissionSummary,
} from "../../services/analyticsService";

const COLORS = ["#2563EB", "#8B5CF6", "#10B981", "#F59E0B", "#EF4444"];

export default function Analytics() {

    const [productsSummary, setProductsSummary] = useState<ProductSummary | null>(null);
    const [scoreDistribution, setScoreDistribution] = useState<ScoreDistribution | null>(null);
    const [commissionDistribution, setCommissionDistribution] = useState<CommissionDistribution | null>(null);
    const [topProducts, setTopProducts] = useState<TopProduct[]>([]);
    const [commissionSummary, setCommissionSummary] = useState<CommissionSummary | null>(null);
    const [salesByRating, setSalesByRating] = useState<Record<string, number> | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    useEffect(() => {

        async function loadData() {

            try {

                setLoading(true);

                const [
                    products,
                    scores,
                    commissions,
                    top,
                    commission,
                    salesRating,
                ] = await Promise.all([
                    getProductsSummary(),
                    getProductsByScore(),
                    getProductsByCommission(),
                    getTopProducts(),
                    getCommissionSummary(),
                    getSalesByRating(),
                ]);

                setProductsSummary(products);
                setScoreDistribution(scores);
                setCommissionDistribution(commissions);
                setTopProducts(top);
                setCommissionSummary(commission);
                setSalesByRating(salesRating);

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

    const scoreData = scoreDistribution ? [
        { name: "80-100", value: scoreDistribution["80-100"] },
        { name: "60-79", value: scoreDistribution["60-79"] },
        { name: "40-59", value: scoreDistribution["40-59"] },
        { name: "0-39", value: scoreDistribution["0-39"] },
    ] : [];

    const commissionData = commissionDistribution ? [
        { name: "0-5%", value: commissionDistribution["0-5%"] },
        { name: "5-10%", value: commissionDistribution["5-10%"] },
        { name: "10-15%", value: commissionDistribution["10-15%"] },
        { name: "15-20%", value: commissionDistribution["15-20%"] },
        { name: "20%+", value: commissionDistribution["20%+"] },
    ] : [];

    const topProductsData = topProducts.map(p => ({
        name: p.name.substring(0, 20),
        score: p.score,
        commission: p.commission,
        sales: p.sales,
    }));

    const salesRatingData = salesByRating ? [
        { name: "4.5-5.0", sales: salesByRating["4.5-5.0"] || 0 },
        { name: "4.0-4.4", sales: salesByRating["4.0-4.4"] || 0 },
        { name: "3.5-3.9", sales: salesByRating["3.5-3.9"] || 0 },
        { name: "3.0-3.4", sales: salesByRating["3.0-3.4"] || 0 },
        { name: "0-2.9", sales: salesByRating["0-2.9"] || 0 },
    ] : [];

    return (

        <Box>

            <Typography
                variant="h4"
                fontWeight="bold"
                color="#F8FAFC"
                mb={4}
            >
                Análises & Métricas
            </Typography>

            {/* Resumos */}
            <Grid container spacing={3} mb={4}>

                <Grid item xs={12} md={4}>
                    <Card sx={{ backgroundColor: "#111827", borderRadius: 3, border: "1px solid #1E293B" }}>
                        <CardContent>
                            <Box sx={{ display: "flex", alignItems: "center", gap: 2 }}>
                                <Box sx={{ p: 1.5, borderRadius: 2, backgroundColor: "#2563EB33", color: "#2563EB" }}>
                                    <TrendingUpIcon />
                                </Box>
                                <Box>
                                    <Typography color="#94A3B8" fontSize="0.875rem">Score Médio</Typography>
                                    <Typography variant="h5" fontWeight="bold" color="#F8FAFC">
                                        {productsSummary?.average_score.toFixed(1)}
                                    </Typography>
                                </Box>
                            </Box>
                        </CardContent>
                    </Card>
                </Grid>

                <Grid item xs={12} md={4}>
                    <Card sx={{ backgroundColor: "#111827", borderRadius: 3, border: "1px solid #1E293B" }}>
                        <CardContent>
                            <Box sx={{ display: "flex", alignItems: "center", gap: 2 }}>
                                <Box sx={{ p: 1.5, borderRadius: 2, backgroundColor: "#10B98133", color: "#10B981" }}>
                                    <AttachMoneyIcon />
                                </Box>
                                <Box>
                                    <Typography color="#94A3B8" fontSize="0.875rem">Comissão Total</Typography>
                                    <Typography variant="h5" fontWeight="bold" color="#F8FAFC">
                                        R$ {commissionSummary?.total_commission.toFixed(2)}
                                    </Typography>
                                </Box>
                            </Box>
                        </CardContent>
                    </Card>
                </Grid>

                <Grid item xs={12} md={4}>
                    <Card sx={{ backgroundColor: "#111827", borderRadius: 3, border: "1px solid #1E293B" }}>
                        <CardContent>
                            <Box sx={{ display: "flex", alignItems: "center", gap: 2 }}>
                                <Box sx={{ p: 1.5, borderRadius: 2, backgroundColor: "#F59E0B33", color: "#F59E0B" }}>
                                    <StarIcon />
                                </Box>
                                <Box>
                                    <Typography color="#94A3B8" fontSize="0.875rem">Avaliação Média</Typography>
                                    <Typography variant="h5" fontWeight="bold" color="#F8FAFC">
                                        {productsSummary?.average_rating.toFixed(1)} ★
                                    </Typography>
                                </Box>
                            </Box>
                        </CardContent>
                    </Card>
                </Grid>

            </Grid>

            {/* Gráficos */}
            <Grid container spacing={3}>

                {/* Score Distribution */}
                <Grid item xs={12} md={6}>
                    <Card sx={{ backgroundColor: "#111827", borderRadius: 3, border: "1px solid #1E293B" }}>
                        <CardContent>
                            <Typography variant="h6" fontWeight="bold" color="#F8FAFC" mb={3}>
                                Distribuição de Scores
                            </Typography>
                            <ResponsiveContainer width="100%" height={300}>
                                <PieChart>
                                    <Pie
                                        data={scoreData}
                                        cx="50%"
                                        cy="50%"
                                        labelLine={false}
                                        label={({ name, value }) => `${name}: ${value}`}
                                        outerRadius={80}
                                        fill="#8884d8"
                                        dataKey="value"
                                    >
                                        {scoreData.map((_, index) => (
                                            <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                                        ))}
                                    </Pie>
                                    <Tooltip />
                                </PieChart>
                            </ResponsiveContainer>
                        </CardContent>
                    </Card>
                </Grid>

                {/* Commission Distribution */}
                <Grid item xs={12} md={6}>
                    <Card sx={{ backgroundColor: "#111827", borderRadius: 3, border: "1px solid #1E293B" }}>
                        <CardContent>
                            <Typography variant="h6" fontWeight="bold" color="#F8FAFC" mb={3}>
                                Distribuição de Comissões
                            </Typography>
                            <ResponsiveContainer width="100%" height={300}>
                                <BarChart data={commissionData}>
                                    <CartesianGrid strokeDasharray="3 3" stroke="#1E293B" />
                                    <XAxis dataKey="name" stroke="#94A3B8" />
                                    <YAxis stroke="#94A3B8" />
                                    <Tooltip contentStyle={{ backgroundColor: "#1E293B", border: "1px solid #2563EB" }} />
                                    <Bar dataKey="value" fill="#2563EB" />
                                </BarChart>
                            </ResponsiveContainer>
                        </CardContent>
                    </Card>
                </Grid>

                {/* Top Products */}
                <Grid item xs={12} md={6}>
                    <Card sx={{ backgroundColor: "#111827", borderRadius: 3, border: "1px solid #1E293B" }}>
                        <CardContent>
                            <Typography variant="h6" fontWeight="bold" color="#F8FAFC" mb={3}>
                                Top 10 Produtos por Score
                            </Typography>
                            <ResponsiveContainer width="100%" height={300}>
                                <BarChart data={topProductsData}>
                                    <CartesianGrid strokeDasharray="3 3" stroke="#1E293B" />
                                    <XAxis dataKey="name" stroke="#94A3B8" angle={-45} textAnchor="end" height={80} />
                                    <YAxis stroke="#94A3B8" />
                                    <Tooltip contentStyle={{ backgroundColor: "#1E293B", border: "1px solid #2563EB" }} />
                                    <Legend />
                                    <Bar dataKey="score" fill="#2563EB" />
                                    <Bar dataKey="commission" fill="#10B981" />
                                </BarChart>
                            </ResponsiveContainer>
                        </CardContent>
                    </Card>
                </Grid>

                {/* Sales by Rating */}
                <Grid item xs={12} md={6}>
                    <Card sx={{ backgroundColor: "#111827", borderRadius: 3, border: "1px solid #1E293B" }}>
                        <CardContent>
                            <Typography variant="h6" fontWeight="bold" color="#F8FAFC" mb={3}>
                                Vendas por Avaliação
                            </Typography>
                            <ResponsiveContainer width="100%" height={300}>
                                <LineChart data={salesRatingData}>
                                    <CartesianGrid strokeDasharray="3 3" stroke="#1E293B" />
                                    <XAxis dataKey="name" stroke="#94A3B8" />
                                    <YAxis stroke="#94A3B8" />
                                    <Tooltip contentStyle={{ backgroundColor: "#1E293B", border: "1px solid #2563EB" }} />
                                    <Legend />
                                    <Line type="monotone" dataKey="sales" stroke="#F59E0B" strokeWidth={2} />
                                </LineChart>
                            </ResponsiveContainer>
                        </CardContent>
                    </Card>
                </Grid>

            </Grid>

        </Box>

    );

}
