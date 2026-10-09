import { useEffect, useState } from "react";

import {
    Box,
    Typography,
    Card,
    CardContent,
    Chip,
    CircularProgress,
    Alert,
    Tabs,
    Tab,
    Grid,
    Avatar,
} from "@mui/material";

import RocketLaunchIcon from "@mui/icons-material/RocketLaunch";
import TrendingUpIcon from "@mui/icons-material/TrendingUp";
import MonetizationOnIcon from "@mui/icons-material/MonetizationOn";
import TipsAndUpdatesIcon from "@mui/icons-material/TipsAndUpdates";

import {
    getEmergingProducts,
    getTrendingProducts,
    getHighCommissionProducts,
    getSmartRecommendations,
    type DiscoveryProduct,
} from "../../services/discoveryService";

function ProductCard({ product, badge }: { product: DiscoveryProduct; badge?: string }) {
    return (
        <Card sx={{ backgroundColor: "#1E293B", border: "1px solid #334155", height: "100%" }}>
            <CardContent sx={{ p: 2 }}>
                <Box sx={{ display: "flex", gap: 1.5, mb: 1 }}>
                    <Avatar
                        src={product.image}
                        variant="rounded"
                        sx={{ width: 56, height: 56, border: "1px solid #334155" }}
                    />
                    <Box sx={{ flex: 1, minWidth: 0 }}>
                        <Typography variant="body2" color="#F8FAFC" fontWeight={600} noWrap>
                            {product.name}
                        </Typography>
                        <Typography variant="caption" color="#10B981" fontWeight={700}>
                            R$ {product.price.toFixed(2)}
                        </Typography>
                        {badge && (
                            <Chip
                                label={badge}
                                size="small"
                                sx={{
                                    ml: 1,
                                    height: 18,
                                    fontSize: 10,
                                    backgroundColor: "#F9731622",
                                    color: "#F97316",
                                }}
                            />
                        )}
                    </Box>
                </Box>
                <Box sx={{ display: "flex", gap: 0.5, flexWrap: "wrap" }}>
                    <Chip label={`${product.commission}% comissão`} size="small" sx={{ height: 20, fontSize: 10, backgroundColor: "#10B98122", color: "#10B981" }} />
                    <Chip label={`⭐ ${product.rating}`} size="small" sx={{ height: 20, fontSize: 10, backgroundColor: "#F59E0B22", color: "#F59E0B" }} />
                    <Chip label={`${product.sales} vendas`} size="small" sx={{ height: 20, fontSize: 10, backgroundColor: "#3B82F622", color: "#3B82F6" }} />
                    {product.score > 0 && <Chip label={`Score: ${product.score}`} size="small" sx={{ height: 20, fontSize: 10, backgroundColor: "#8B5CF622", color: "#8B5CF6" }} />}
                    {product.opportunity_index && <Chip label={`OI: ${product.opportunity_index}`} size="small" sx={{ height: 20, fontSize: 10, backgroundColor: "#F9731622", color: "#F97316" }} />}
                </Box>
            </CardContent>
        </Card>
    );
}

export default function Discovery() {
    const [tab, setTab] = useState(0);
    const [emerging, setEmerging] = useState<DiscoveryProduct[]>([]);
    const [trending, setTrending] = useState<DiscoveryProduct[]>([]);
    const [highComm, setHighComm] = useState<DiscoveryProduct[]>([]);
    const [recs, setRecs] = useState<{ emerging: DiscoveryProduct[]; top_performers: DiscoveryProduct[]; high_profit: DiscoveryProduct[] } | null>(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    async function load() {
        try {
            setLoading(true);
            setError("");
            if (tab === 0) setEmerging(await getEmergingProducts());
            else if (tab === 1) setTrending(await getTrendingProducts());
            else if (tab === 2) setHighComm(await getHighCommissionProducts());
            else if (tab === 3) setRecs(await getSmartRecommendations());
        } catch (err) {
            console.error("[Discovery] Erro ao carregar:", err);
            setError("Erro ao carregar dados. Tente novamente.");
        } finally {
            setLoading(false);
        }
    }

    useEffect(() => { load(); }, [tab]);

    const tabItems = [
        { label: "Emergentes", icon: <RocketLaunchIcon /> },
        { label: "Trending", icon: <TrendingUpIcon /> },
        { label: "Alta Comissão", icon: <MonetizationOnIcon /> },
        { label: "Recomendações IA", icon: <TipsAndUpdatesIcon /> },
    ];

    function renderProducts(products: DiscoveryProduct[], badge?: string) {
        if (!products.length) return <Typography color="#94A3B8">Nenhum produto encontrado.</Typography>;
        return (
            <Grid container spacing={2}>
                {products.map((p) => (
                    <Grid item xs={12} sm={6} md={4} lg={3} key={p.id}>
                        <ProductCard product={p} badge={badge || p.tag} />
                    </Grid>
                ))}
            </Grid>
        );
    }

    return (
        <Box>
            <Typography variant="h5" fontWeight="bold" color="#F8FAFC" gutterBottom>
                Descoberta de Produtos
            </Typography>
            <Typography variant="body2" color="#94A3B8" sx={{ mb: 3 }}>
                Estratégia "Loophole": encontre produtos emergentes com alta comissão e baixa concorrência
            </Typography>

            {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}

            <Tabs
                value={tab}
                onChange={(_, v) => setTab(v)}
                sx={{ mb: 3, "& .MuiTab-root": { color: "#94A3B8" }, "& .Mui-selected": { color: "#F97316" }, "& .MuiTabs-indicator": { backgroundColor: "#F97316" } }}
            >
                {tabItems.map((t, i) => <Tab key={i} label={t.label} icon={t.icon} iconPosition="start" />)}
            </Tabs>

            {loading ? (
                <Box sx={{ display: "flex", justifyContent: "center", pt: 6 }}><CircularProgress sx={{ color: "#F97316" }} /></Box>
            ) : (
                <>
                    {tab === 0 && renderProducts(emerging, "EMERGENTE")}
                    {tab === 1 && renderProducts(trending, "TRENDING")}
                    {tab === 2 && renderProducts(highComm, "ALTA COMISSÃO")}
                    {tab === 3 && recs && (
                        <Box>
                            <Typography variant="h6" color="#F8FAFC" sx={{ mb: 2 }}>🚀 Emergentes</Typography>
                            {renderProducts(recs.emerging)}
                            <Typography variant="h6" color="#F8FAFC" sx={{ mt: 3, mb: 2 }}>🏆 Top Performers</Typography>
                            {renderProducts(recs.top_performers)}
                            <Typography variant="h6" color="#F8FAFC" sx={{ mt: 3, mb: 2 }}>💰 Alta Comissão</Typography>
                            {renderProducts(recs.high_profit)}
                        </Box>
                    )}
                </>
            )}
        </Box>
    );
}
