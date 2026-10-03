import { useEffect, useState } from "react";
import {
    Alert,
    Box,
    Button,
    Card,
    CardContent,
    Chip,
    CircularProgress,
    Dialog,
    DialogActions,
    DialogContent,
    DialogContentText,
    DialogTitle,
    Grid,
    Link,
    Paper,
    Snackbar,
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow,
    TextField,
    Typography,
} from "@mui/material";
import {
    AddCircleOutline,
    CheckCircle,
    DeleteOutline,
    ErrorOutline,
    LinkOff,
    Sync,
} from "@mui/icons-material";

import {
    connectAccount,
    disconnectAccount,
    listAvailableMarketplaces,
    listMyAccounts,
    updateAccount,
    type MarketplaceAccountItem,
} from "../../services/marketplaceAccountService";
import { getData } from "../../services/apiResponse";

const MARKETPLACE_INFO: Record<string, { label: string; color: string }> = {
    shopee: { label: "Shopee", color: "#EE4D2D" },
    mercado_livre: { label: "Mercado Livre", color: "#FFE600" },
    amazon: { label: "Amazon", color: "#FF9900" },
    aliexpress: { label: "AliExpress", color: "#E62E04" },
    magalu: { label: "Magalu", color: "#0086FF" },
    tiktok: { label: "TikTok Shop", color: "#25F4EE" },
};

function marketplaceLabel(name: string): string {
    const info = MARKETPLACE_INFO[name];
    if (info) {
        return info.label;
    }
    return name.charAt(0).toUpperCase() + name.slice(1).replace("_", " ");
}

function statusChip(status: string) {
    const ok = status === "conectada";
    return (
        <Chip
            size="small"
            icon={ok ? <CheckCircle /> : <ErrorOutline />}
            label={ok ? "Conectada" : status}
            sx={{
                color: ok ? "#10B981" : "#F59E0B",
                backgroundColor: ok ? "rgba(16,185,129,0.12)" : "rgba(245,158,11,0.12)",
                fontWeight: 600,
            }}
        />
    );
}

export default function Accounts() {
    const [accounts, setAccounts] = useState<MarketplaceAccountItem[]>([]);
    const [available, setAvailable] = useState<string[]>([]);
    const [loading, setLoading] = useState(true);
    const [saving, setSaving] = useState(false);
    const [error, setError] = useState("");
    const [toast, setToast] = useState("");

    const [openConnect, setOpenConnect] = useState(false);
    const [target, setTarget] = useState("");
    const [appId, setAppId] = useState("");
    const [secret, setSecret] = useState("");

    const [openDisconnect, setOpenDisconnect] = useState("");
    const [removing, setRemoving] = useState(false);

    async function load() {
        setLoading(true);
        setError("");
        try {
            const [accountList, marketplaces] = await Promise.all([
                listMyAccounts(),
                listAvailableMarketplaces(),
            ]);
            setAccounts(accountList);
            setAvailable(marketplaces);
        } catch (e: unknown) {
            setError(
                e instanceof Error ? e.message : "Erro ao carregar contas."
            );
        } finally {
            setLoading(false);
        }
    }

    useEffect(() => {
        void load();
    }, []);

    function openConnectFor(name: string) {
        setTarget(name);
        setAppId("");
        setSecret("");
        setError("");
        setOpenConnect(true);
    }

    async function handleConnect() {
        if (!appId.trim() || !secret.trim()) {
            setError("Informe o App ID e o Secret da sua conta de afiliado.");
            return;
        }
        setSaving(true);
        setError("");
        try {
            const payload = {
                marketplace: target,
                extra: JSON.stringify({
                    app_id: appId.trim(),
                    secret: secret.trim(),
                }),
            };
            const alreadyConnected = accounts.some(
                (a) => a.marketplace === target && a.is_active
            );
            if (alreadyConnected) {
                await updateAccount(target, { extra: payload.extra });
                setToast("Credenciais atualizadas com sucesso.");
            } else {
                await connectAccount(payload);
                setToast("Conta conectada com sucesso.");
            }
            setOpenConnect(false);
            await load();
        } catch (e: unknown) {
            setError(
                e instanceof Error ? e.message : "Falha ao conectar a conta."
            );
        } finally {
            setSaving(false);
        }
    }

    async function handleAuthorizeMercadoLivre() {
        setError("");
        try {
            const result = await getData<{ authorize_url: string }>(
                "/mercadolivre/authorize-url"
            );
            window.location.href = result.authorize_url;
        } catch (e: unknown) {
            setError(
                e instanceof Error
                    ? e.message
                    : "Falha ao gerar o link de autorização do Mercado Livre."
            );
        }
    }

    async function handleDisconnect() {
        setRemoving(true);
        try {
            await disconnectAccount(openDisconnect);
            setOpenDisconnect("");
            setToast("Conta desconectada.");
            await load();
        } catch (e: unknown) {
            setToast(
                e instanceof Error ? e.message : "Falha ao desconectar."
            );
        } finally {
            setRemoving(false);
        }
    }

    return (
        <Box>
            <Typography variant="h4" fontWeight={700} color="#F8FAFC" gutterBottom>
                Contas de Afiliado
            </Typography>
            <Typography color="#94A3B8" mb={3}>
                Conecte as contas dos marketplaces para rastrear suas vendas e
                gerar links de afiliado com as suas credenciais.
            </Typography>

            {error && (
                <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError("")}>
                    {error}
                </Alert>
            )}

            {loading ? (
                <Box display="flex" justifyContent="center" py={6}>
                    <CircularProgress />
                </Box>
            ) : (
                <Grid container spacing={2}>
                    {accounts.map((account) => {
                        const info = MARKETPLACE_INFO[account.marketplace] || {};
                        return (
                            <Grid item xs={12} sm={6} md={4} key={account.id}>
                                <Card sx={{ backgroundColor: "#111827", borderRadius: 3 }}>
                                    <CardContent>
                                        <Box
                                            display="flex"
                                            alignItems="center"
                                            justifyContent="space-between"
                                            mb={1}
                                        >
                                            <Typography
                                                fontWeight={700}
                                                color="#F8FAFC"
                                                sx={{
                                                    display: "flex",
                                                    alignItems: "center",
                                                    gap: 1,
                                                }}
                                            >
                                                <Box
                                                    component="span"
                                                    sx={{
                                                        width: 10,
                                                        height: 10,
                                                        borderRadius: "50%",
                                                        backgroundColor:
                                                            info.color || "#2563EB",
                                                        display: "inline-block",
                                                    }}
                                                />
                                                {marketplaceLabel(account.marketplace)}
                                            </Typography>
                                            {statusChip(account.status)}
                                        </Box>
                                        <Typography
                                            variant="body2"
                                            color="#94A3B8"
                                            mb={2}
                                        >
                                            {account.has_access_token
                                                ? "Token armazenado (criptografado)"
                                                : "Credenciais configuradas"}
                                        </Typography>
                                        <Box display="flex" gap={1}>
                                            {account.marketplace === "mercado_livre" && (
                                                <Button
                                                    size="small"
                                                    variant="contained"
                                                    onClick={handleAuthorizeMercadoLivre}
                                                >
                                                    Autorizar no Mercado Livre
                                                </Button>
                                            )}
                                            <Button
                                                size="small"
                                                variant="outlined"
                                                startIcon={<LinkOff />}
                                                color="error"
                                                onClick={() =>
                                                    setOpenDisconnect(account.marketplace)
                                                }
                                            >
                                                Desconectar
                                            </Button>
                                        </Box>
                                    </CardContent>
                                </Card>
                            </Grid>
                        );
                    })}

                    {accounts.length === 0 && (
                        <Grid item xs={12}>
                            <Alert severity="info">
                                Nenhuma conta conectada ainda.
                            </Alert>
                        </Grid>
                    )}
                </Grid>
            )}

            <Typography variant="h6" fontWeight={700} color="#F8FAFC" mt={5} mb={2}>
                Marketplaces disponíveis
            </Typography>
            <TableContainer component={Paper} sx={{ backgroundColor: "#111827" }}>
                <Table size="small">
                    <TableHead>
                        <TableRow>
                            <TableCell>Marketplace</TableCell>
                            <TableCell>Status</TableCell>
                            <TableCell align="right">Ação</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {available.map((name) => {
                            const connected = accounts.some(
                                (a) => a.marketplace === name && a.is_active
                            );
                            const info = MARKETPLACE_INFO[name] || {};
                            return (
                                <TableRow key={name}>
                                    <TableCell>
                                        <Typography
                                            color="#F8FAFC"
                                            sx={{
                                                display: "flex",
                                                alignItems: "center",
                                                gap: 1,
                                            }}
                                        >
                                            <Box
                                                component="span"
                                                sx={{
                                                    width: 10,
                                                    height: 10,
                                                    borderRadius: "50%",
                                                    backgroundColor:
                                                        info.color || "#2563EB",
                                                    display: "inline-block",
                                                }}
                                            />
                                            {marketplaceLabel(name)}
                                        </Typography>
                                    </TableCell>
                                    <TableCell>
                                        {connected ? (
                                            statusChip("conectada")
                                        ) : (
                                            <Chip
                                                size="small"
                                                label="Não conectada"
                                                sx={{ color: "#94A3B8" }}
                                            />
                                        )}
                                    </TableCell>
                                    <TableCell align="right">
                                        {connected ? (
                                            <Button
                                                size="small"
                                                startIcon={<Sync />}
                                                onClick={() => openConnectFor(name)}
                                            >
                                                Atualizar
                                            </Button>
                                        ) : (
                                            <Button
                                                size="small"
                                                variant="contained"
                                                startIcon={<AddCircleOutline />}
                                                onClick={() => openConnectFor(name)}
                                            >
                                                Conectar
                                            </Button>
                                        )}
                                    </TableCell>
                                </TableRow>
                            );
                        })}
                    </TableBody>
                </Table>
            </TableContainer>

            <Typography variant="body2" color="#64748B" mt={2}>
                Para encontrar suas credenciais Shopee, acesse o{" "}
                <Link
                    href="https://affiliate.shopee.com.br"
                    target="_blank"
                    rel="noreferrer"
                    color="primary"
                >
                    Portal do Afiliado Shopee
                </Link>{" "}
                → Open API → Application. Mercado Livre, Amazon e outros
                marketplaces estarão disponíveis em breve.
            </Typography>

            <Dialog open={openConnect} onClose={() => setOpenConnect(false)}>
                <DialogTitle>
                    Conectar {marketplaceLabel(target)}
                </DialogTitle>
                <DialogContent>
                    <DialogContentText mb={2} color="#94A3B8">
                        Informe as credenciais da sua conta de afiliado no{" "}
                        {marketplaceLabel(target)}. Elas ficam criptografadas
                        no banco de dados e são usadas para assinar suas
                        requisições.
                    </DialogContentText>
                    <TextField
                        label="App ID"
                        fullWidth
                        value={appId}
                        onChange={(e) => setAppId(e.target.value)}
                        margin="dense"
                    />
                    <TextField
                        label="Secret"
                        fullWidth
                        value={secret}
                        onChange={(e) => setSecret(e.target.value)}
                        margin="dense"
                        type="password"
                    />
                    {error && (
                        <Alert severity="error" sx={{ mt: 2 }}>
                            {error}
                        </Alert>
                    )}
                </DialogContent>
                <DialogActions>
                    <Button onClick={() => setOpenConnect(false)}>
                        Cancelar
                    </Button>
                    <Button
                        variant="contained"
                        onClick={handleConnect}
                        disabled={saving}
                    >
                        {saving ? "Conectando..." : "Conectar"}
                    </Button>
                </DialogActions>
            </Dialog>

            <Dialog open={Boolean(openDisconnect)} onClose={() => setOpenDisconnect("")}>
                <DialogTitle>Desconectar conta</DialogTitle>
                <DialogContent>
                    <DialogContentText color="#94A3B8">
                        Deseja realmente desconectar a conta de{" "}
                        {marketplaceLabel(openDisconnect)}? As vendas já
                        registradas continuam no seu histórico.
                    </DialogContentText>
                </DialogContent>
                <DialogActions>
                    <Button onClick={() => setOpenDisconnect("")}>Cancelar</Button>
                    <Button
                        color="error"
                        variant="contained"
                        onClick={handleDisconnect}
                        disabled={removing}
                        startIcon={<DeleteOutline />}
                    >
                        Desconectar
                    </Button>
                </DialogActions>
            </Dialog>

            <Snackbar
                open={Boolean(toast)}
                autoHideDuration={4000}
                onClose={() => setToast("")}
                message={toast}
            />
        </Box>
    );
}
