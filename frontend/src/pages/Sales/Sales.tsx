import { useEffect, useState } from "react";

import {
    Box,
    Typography,
    Grid,
    Card,
    CardContent,
    Chip,
    Button,
    CircularProgress,
    Alert,
    Tabs,
    Tab,
    Snackbar,
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow,
    Paper,
} from "@mui/material";

import SyncIcon from "@mui/icons-material/Sync";
import AttachMoneyIcon from "@mui/icons-material/AttachMoney";
import ReceiptLongIcon from "@mui/icons-material/ReceiptLong";
import LinkIcon from "@mui/icons-material/Link";

import {
    syncSales,
    listSales,
    getFinancialSummary,
    getCampaignTracking,
    type SaleItem,
    type FinancialSummary,
    type CampaignTracking,
} from "../../services/salesService";

function statusColor(status: string) {
    if (status === "confirmada" || status === "PUBLISHED") return "#10B981";
    if (status === "pendente" || status === "DRAFT") return "#F59E0B";
    if (status === "cancelada") return "#EF4444";
    return "#94A3B8";
}

export default function Sales() {

    const [tab, setTab] = useState(0);
    const [sales, setSales] = useState<SaleItem[]>([]);
    const [financial, setFinancial] = useState<FinancialSummary | null>(null);
    const [campaigns, setCampaigns] = useState<CampaignTracking[]>([]);
    const [loading, setLoading] = useState(false);
    const [syncing, setSyncing] = useState(false);
    const [error, setError] = useState("");
    const [toast, setToast] = useState("");

    async function loadFinancial() {
        try {
            setLoading(true);
            const [fin, salesData] = await Promise.all([
                getFinancialSummary(),
                listSales(),
            ]);
            setFinancial(fin);
            setSales(salesData);
        } catch {
            setError("Erro ao carregar dados financeiros.");
        } finally {
            setLoading(false);
        }
    }

    async function loadCampaigns() {
        try {
            setLoading(true);
            const data = await getCampaignTracking();
            setCampaigns(data);
        } catch {
            setError("Erro ao carregar campanhas.");
        } finally {
            setLoading(false);
        }
    }

    useEffect(() => {
        if (tab === 0) loadFinancial();
        else loadCampaigns();
    }, [tab]);

    async function handleSync() {
        try {
            setSyncing(true);
            const result = await syncSales(7);
            setToast(`Sincronizado: ${result.new_sales} nova(s), ${result.updated_sales} atualizada(s).`);
            loadFinancial();
        } catch {
            setToast("Erro ao sincronizar com a Shopee.");
        } finally {
            setSyncing(false);
        }
    }

    const cardSx = { backgroundColor: "#111827", borderRadius: 3, border: "1px solid #1E293B" };

    return (

        <Box>

            <Box sx={{ display: "flex", alignItems: "center", gap: 1.5, mb: 1 }}>
                <AttachMoneyIcon sx={{ color: "#10B981" }} />
                <Typography variant="h4" fontWeight="bold" color="#F8FAFC">
                    Vendas & Comissoes
                </Typography>
            </Box>

            <Typography color="#94A3B8" mb={3}>
                Acompanhe suas vendas, comissoes e status de divulgacao em tempo real.
                A comissao e creditada diretamente na sua conta Shopee Affiliate.
            </Typography>

            <Tabs
                value={tab}
                onChange={(_, v) => setTab(v)}
                sx={{ mb: 3, borderBottom: "1px solid #1E293B" }}
            >
                <Tab label="Painel Financeiro" sx={{ color: "#94A3B8" }} />
                <Tab label="Rastreamento de Campanhas" sx={{ color: "#94A3B8" }} />
            </Tabs>

            {loading && (
                <Box display="flex" justifyContent="center" py={6}>
                    <CircularProgress />
                </Box>
            )}

            {!loading && error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}

            {!loading && tab === 0 && (
                <>
                    <Box sx={{ mb: 3 }}>
                        <Button
                            variant="contained"
                            startIcon={syncing ? <CircularProgress size={18} /> : <SyncIcon />}
                            onClick={handleSync}
                            disabled={syncing}
                        >
                            Sincronizar com Shopee
                        </Button>
                    </Box>

                    {financial && (
                        <Grid container spacing={3} sx={{ mb: 4 }}>
                            <Grid item xs={12} sm={6} md={3}>
                                <Card sx={cardSx}>
                                    <CardContent>
                                        <Typography variant="caption" color="#94A3B8">Total de Vendas</Typography>
                                        <Typography variant="h4" fontWeight="bold" color="#F8FAFC">
                                            {financial.total_sales}
                                        </Typography>
                                    </CardContent>
                                </Card>
                            </Grid>
                            <Grid item xs={12} sm={6} md={3}>
                                <Card sx={cardSx}>
                                    <CardContent>
                                        <Typography variant="caption" color="#94A3B8">Comissao Total</Typography>
                                        <Typography variant="h4" fontWeight="bold" color="#10B981">
                                            R$ {financial.total_commission.toFixed(2)}
                                        </Typography>
                                    </CardContent>
                                </Card>
                            </Grid>
                            <Grid item xs={12} sm={6} md={3}>
                                <Card sx={cardSx}>
                                    <CardContent>
                                        <Typography variant="caption" color="#F59E0B">Pendente</Typography>
                                        <Typography variant="h4" fontWeight="bold" color="#F59E0B">
                                            R$ {financial.pending_amount.toFixed(2)}
                                        </Typography>
                                        <Typography variant="caption" color="#94A3B8">
                                            {financial.pending_count} venda(s)
                                        </Typography>
                                    </CardContent>
                                </Card>
                            </Grid>
                            <Grid item xs={12} sm={6} md={3}>
                                <Card sx={cardSx}>
                                    <CardContent>
                                        <Typography variant="caption" color="#10B981">Disponivel para Saque</Typography>
                                        <Typography variant="h4" fontWeight="bold" color="#10B981">
                                            R$ {financial.available_to_withdraw.toFixed(2)}
                                        </Typography>
                                        <Typography variant="caption" color="#94A3B8">
                                            {financial.confirmed_count} confirmada(s)
                                        </Typography>
                                    </CardContent>
                                </Card>
                            </Grid>
                        </Grid>
                    )}

                    <Typography variant="h6" color="#F8FAFC" mb={2} sx={{ display: "flex", alignItems: "center", gap: 1 }}>
                        <ReceiptLongIcon /> Historico de Vendas
                    </Typography>

                    {sales.length === 0 ? (
                        <Alert severity="info">
                            Nenhuma venda registrada ainda. Clique em "Sincronizar com Shopee" para buscar
                            suas conversoes, ou aguarde vendas dos seus links de afiliado.
                        </Alert>
                    ) : (
                        <TableContainer component={Paper} sx={{ backgroundColor: "#111827", borderRadius: 2 }}>
                            <Table size="small">
                                <TableHead>
                                    <TableRow>
                                        <TableCell sx={{ color: "#94A3B8" }}>Pedido</TableCell>
                                        <TableCell sx={{ color: "#94A3B8" }}>Status</TableCell>
                                        <TableCell sx={{ color: "#94A3B8" }}>Compra</TableCell>
                                        <TableCell sx={{ color: "#94A3B8" }}>Dispositivo</TableCell>
                                        <TableCell sx={{ color: "#94A3B8" }}>Comissao</TableCell>
                                        <TableCell sx={{ color: "#94A3B8" }}>Liquido</TableCell>
                                    </TableRow>
                                </TableHead>
                                <TableBody>
                                    {sales.map((s) => (
                                        <TableRow key={s.id}>
                                            <TableCell sx={{ color: "#F8FAFC" }}>{s.order_id || s.conversion_id}</TableCell>
                                            <TableCell>
                                                <Chip
                                                    label={s.status}
                                                    size="small"
                                                    sx={{ backgroundColor: statusColor(s.status), color: "#0B1120", fontWeight: 700 }}
                                                />
                                            </TableCell>
                                            <TableCell sx={{ color: "#94A3B8" }}>{s.purchase_time}</TableCell>
                                            <TableCell sx={{ color: "#94A3B8" }}>{s.device}</TableCell>
                                            <TableCell sx={{ color: "#F8FAFC" }}>R$ {s.total_commission.toFixed(2)}</TableCell>
                                            <TableCell sx={{ color: "#10B981", fontWeight: 700 }}>
                                                R$ {s.net_commission.toFixed(2)}
                                            </TableCell>
                                        </TableRow>
                                    ))}
                                </TableBody>
                            </Table>
                        </TableContainer>
                    )}
                </>
            )}

            {!loading && tab === 1 && (
                <>
                    <Typography variant="h6" color="#F8FAFC" mb={2} sx={{ display: "flex", alignItems: "center", gap: 1 }}>
                        <LinkIcon /> Campanhas com Rastreamento
                    </Typography>

                    {campaigns.length === 0 ? (
                        <Alert severity="info">
                            Nenhuma campanha com link de rastreamento. Gere links na aba Oportunidades
                            para acompanhar cliques e conversoes.
                        </Alert>
                    ) : (
                        <Grid container spacing={3}>
                            {campaigns.map((c) => (
                                <Grid item xs={12} md={6} key={c.id}>
                                    <Card sx={cardSx}>
                                        <CardContent>
                                            <Box sx={{ display: "flex", justifyContent: "space-between", mb: 1 }}>
                                                <Chip
                                                    label={c.status}
                                                    size="small"
                                                    sx={{ backgroundColor: statusColor(c.status), color: "#0B1120", fontWeight: 700 }}
                                                />
                                            </Box>
                                            <Typography fontWeight="bold" color="#F8FAFC" mb={1}>
                                                {c.title}
                                            </Typography>
                                            <Typography variant="body2" color="#94A3B8" mb={1}>
                                                Canal: {c.channel}
                                            </Typography>
                                            {c.tracking_link && (
                                                <Typography variant="caption" color="#2563EB" display="block" mb={1}
                                                    sx={{ wordBreak: "break-all" }}>
                                                    Link: {c.tracking_link}
                                                </Typography>
                                            )}
                                            <Box sx={{ display: "flex", gap: 3, mt: 1 }}>
                                                <Box>
                                                    <Typography variant="caption" color="#94A3B8">Cliques</Typography>
                                                    <Typography fontWeight="bold" color="#F8FAFC">{c.clicks}</Typography>
                                                </Box>
                                                <Box>
                                                    <Typography variant="caption" color="#94A3B8">Conversoes</Typography>
                                                    <Typography fontWeight="bold" color="#F8FAFC">{c.conversions}</Typography>
                                                </Box>
                                                <Box>
                                                    <Typography variant="caption" color="#94A3B8">Receita</Typography>
                                                    <Typography fontWeight="bold" color="#10B981">
                                                        R$ {c.revenue.toFixed(2)}
                                                    </Typography>
                                                </Box>
                                            </Box>
                                        </CardContent>
                                    </Card>
                                </Grid>
                            ))}
                        </Grid>
                    )}
                </>
            )}

            <Snackbar
                open={!!toast}
                autoHideDuration={4000}
                onClose={() => setToast("")}
                message={toast}
            />

        </Box>

    );

}
