import { useEffect, useState } from "react";

import {
    Box,
    Grid,
    Typography,
    Card,
    CardContent,
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow,
    Avatar,
    Chip,
    CircularProgress,
    Alert,
    Button,
} from "@mui/material";

import InventoryIcon from "@mui/icons-material/Inventory2";
import TrendingUpIcon from "@mui/icons-material/TrendingUp";
import AttachMoneyIcon from "@mui/icons-material/AttachMoney";
import SmartToyIcon from "@mui/icons-material/SmartToy";
import OpenInNewIcon from "@mui/icons-material/OpenInNew";
import ArrowForwardIcon from "@mui/icons-material/ArrowForward";

import StatCard from "../../components/dashboard/StatCard";
import HealthCard from "../../components/health/HealthCard";

import { getDashboard, getHealth } from "../../services/dashboardService";
import type { DashboardStats } from "../../services/dashboardService";
import { searchShopeeProducts, type ShopeeProductNode } from "../../services/marketplaceService";

import { Link } from "react-router-dom";

export default function Dashboard() {

    const [dashboard, setDashboard] = useState<DashboardStats | null>(null);
    const [health, setHealth] = useState<Record<string, string> | null>(null);
    const [products, setProducts] = useState<ShopeeProductNode[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    useEffect(() => {

        async function loadData() {

            try {

                setLoading(true);

                const [dashboardData, healthData, productsData] = await Promise.all([
                    getDashboard(),
                    getHealth(),
                    searchShopeeProducts({ keyword: "tendencia", limit: 5 }),
                ]);

                setDashboard(dashboardData);
                setHealth(healthData);
                setProducts(productsData.nodes || []);

                setError("");

            } catch (err) {

                console.error(err);
                setError("Erro ao carregar dados do painel.");

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

    return (

        <Box>

            <Box
                sx={{
                    display: "flex",
                    justifyContent: "space-between",
                    alignItems: "center",
                    mb: 4,
                }}
            >

                <Typography
                    variant="h4"
                    fontWeight="bold"
                    color="#F8FAFC"
                >
                    Painel de Controle
                </Typography>

                <Typography
                    variant="body2"
                    color="#94A3B8"
                >
                    v{dashboard?.version || "2.0"}
                </Typography>

            </Box>

            <Grid container spacing={3} mb={4}>

                <Grid item xs={12} sm={6} md={3}>
                    <StatCard
                        title="Produtos Rastreados"
                        value={dashboard?.total_products || 0}
                        subtitle="No banco de dados"
                        icon={InventoryIcon}
                        color="#38BDF8"
                    />
                </Grid>

                <Grid item xs={12} sm={6} md={3}>
                    <StatCard
                        title="Pipeline IA"
                        value={dashboard?.pipeline || "READY"}
                        subtitle="Status operacional"
                        icon={SmartToyIcon}
                        color="#8B5CF6"
                    />
                </Grid>

                <Grid item xs={12} sm={6} md={3}>
                    <StatCard
                        title="Status do Sistema"
                        value={dashboard?.status || "online"}
                        subtitle="Backend ativo"
                        icon={TrendingUpIcon}
                        color="#10B981"
                    />
                </Grid>

                <Grid item xs={12} sm={6} md={3}>
                    <StatCard
                        title="Shopee API"
                        value={products.length > 0 ? "Conectada" : "Verificando"}
                        subtitle={products.length > 0 ? `${products.length} produtos carregados` : "Aguardando dados"}
                        icon={AttachMoneyIcon}
                        color={products.length > 0 ? "#F59E0B" : "#EF4444"}
                    />
                </Grid>

            </Grid>

            <Grid container spacing={3} mb={4}>

                <Grid item xs={12} md={8}>

                    <Card
                        sx={{
                            background: "#111827",
                            borderRadius: 3,
                            border: "1px solid #1E293B",
                            height: "100%",
                        }}
                    >

                        <CardContent>

                            <Box
                                sx={{
                                    display: "flex",
                                    justifyContent: "space-between",
                                    alignItems: "center",
                                    mb: 3,
                                }}
                            >

                                <Typography
                                    variant="h6"
                                    fontWeight="bold"
                                    color="#F8FAFC"
                                >
                                    Produtos em Destaque - Shopee
                                </Typography>

                                <Button
                                    component={Link}
                                    to="/products"
                                    endIcon={<ArrowForwardIcon />}
                                    sx={{
                                        color: "#38BDF8",
                                        textTransform: "none",
                                    }}
                                >
                                    Ver todos
                                </Button>

                            </Box>

                            <TableContainer>

                                <Table size="small">

                                    <TableHead>
                                        <TableRow>
                                            <TableCell sx={{ color: "#94A3B8" }}>Produto</TableCell>
                                            <TableCell sx={{ color: "#94A3B8" }}>Preço</TableCell>
                                            <TableCell sx={{ color: "#94A3B8" }}>Comissão</TableCell>
                                            <TableCell sx={{ color: "#94A3B8" }}>Vendas</TableCell>
                                            <TableCell sx={{ color: "#94A3B8" }}>Ação</TableCell>
                                        </TableRow>
                                    </TableHead>

                                    <TableBody>

                                        {products.map((product) => (

                                            <TableRow
                                                key={product.itemId}
                                                sx={{
                                                    "&:hover": {
                                                        backgroundColor: "#1E293B",
                                                    },
                                                }}
                                            >

                                                <TableCell>
                                                    <Box
                                                        sx={{
                                                            display: "flex",
                                                            alignItems: "center",
                                                            gap: 2,
                                                        }}
                                                    >
                                                        <Avatar
                                                            src={product.imageUrl}
                                                            alt={product.productName}
                                                            variant="rounded"
                                                            sx={{ width: 40, height: 40 }}
                                                        />
                                                        <Typography
                                                            color="#F8FAFC"
                                                            sx={{
                                                                maxWidth: 300,
                                                                overflow: "hidden",
                                                                textOverflow: "ellipsis",
                                                                whiteSpace: "nowrap",
                                                            }}
                                                        >
                                                            {product.productName}
                                                        </Typography>
                                                    </Box>
                                                </TableCell>

                                                <TableCell>
                                                    <Typography color="#F8FAFC">
                                                        R$ {product.price}
                                                    </Typography>
                                                </TableCell>

                                                <TableCell>
                                                    <Chip
                                                        label={`${Math.round(parseFloat(product.commissionRate) * 100)}%`}
                                                        size="small"
                                                        sx={{
                                                            backgroundColor: "#10B98133",
                                                            color: "#10B981",
                                                            fontWeight: 600,
                                                        }}
                                                    />
                                                </TableCell>

                                                <TableCell>
                                                    <Typography color="#F8FAFC">
                                                        {product.sales}
                                                    </Typography>
                                                </TableCell>

                                                <TableCell>
                                                    <Button
                                                        href={product.offerLink}
                                                        target="_blank"
                                                        rel="noopener noreferrer"
                                                        size="small"
                                                        endIcon={<OpenInNewIcon />}
                                                        sx={{
                                                            color: "#38BDF8",
                                                            textTransform: "none",
                                                        }}
                                                    >
                                                        Oferta
                                                    </Button>
                                                </TableCell>

                                            </TableRow>

                                        ))}

                                    </TableBody>

                                </Table>

                            </TableContainer>

                        </CardContent>

                    </Card>

                </Grid>

                <Grid item xs={12} md={4}>

                    <Card
                        sx={{
                            background: "#111827",
                            borderRadius: 3,
                            border: "1px solid #1E293B",
                            height: "100%",
                        }}
                    >

                        <CardContent>

                            <Typography
                                variant="h6"
                                fontWeight="bold"
                                color="#F8FAFC"
                                mb={3}
                            >
                                Saúde do Sistema
                            </Typography>

                            <Grid container spacing={2}>

                                {health && Object.entries(health).map(([key, value]) => (

                                    <Grid item xs={12} key={key}>
                                        <HealthCard
                                            title={key.replace(/_/g, " ").toUpperCase()}
                                            status={String(value)}
                                        />
                                    </Grid>

                                ))}

                            </Grid>

                        </CardContent>

                    </Card>

                </Grid>

            </Grid>

        </Box>

    );

}
