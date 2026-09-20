import { useEffect, useRef, useState } from "react";

import {
    Box,
    Typography,
    Card,
    CardContent,
    Button,
    CircularProgress,
    Alert,
    TextField,
    Grid,
    List,
    ListItemButton,
    ListItemText,
    Chip,
    Divider,
} from "@mui/material";

import QrCode2Icon from "@mui/icons-material/QrCode2";
import SendIcon from "@mui/icons-material/Send";
import PowerSettingsNewIcon from "@mui/icons-material/PowerSettingsNew";

import {
    startSession,
    getQrCode,
    getSessionStatus,
    stopSession,
    listConversations,
    listMessages,
    sendMessage,
    type WhatsAppConversation,
    type WhatsAppMessageItem,
    type WhatsAppSessionStatus,
} from "../../services/whatsappService";

export default function WhatsApp() {
    const [status, setStatus] = useState<WhatsAppSessionStatus | null>(null);
    const [qrCode, setQrCode] = useState("");
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(true);
    const [connecting, setConnecting] = useState(false);

    const [conversations, setConversations] = useState<WhatsAppConversation[]>([]);
    const [selectedPhone, setSelectedPhone] = useState<string | null>(null);
    const [messages, setMessages] = useState<WhatsAppMessageItem[]>([]);
    const [draft, setDraft] = useState("");
    const [sending, setSending] = useState(false);

    const pollRef = useRef<number | null>(null);

    async function loadStatus() {
        try {
            const s = await getSessionStatus();
            setStatus(s);
            return s;
        } catch {
            setError("Não foi possível consultar o status da sessão.");
            return null;
        }
    }

    async function loadConversations() {
        try {
            const list = await listConversations();
            setConversations(list);
        } catch {
            // silencioso: lista de conversas depende do backend/WAHA estarem de pé
        }
    }

    async function loadMessages(phone: string) {
        try {
            const list = await listMessages(phone);
            setMessages(list);
        } catch {
            setError("Erro ao carregar mensagens.");
        }
    }

    useEffect(() => {
        (async () => {
            setLoading(true);
            await loadStatus();
            await loadConversations();
            setLoading(false);
        })();

        pollRef.current = window.setInterval(() => {
            loadStatus();
            loadConversations();
        }, 8000);

        return () => {
            if (pollRef.current) window.clearInterval(pollRef.current);
        };
    }, []);

    useEffect(() => {
        if (selectedPhone) loadMessages(selectedPhone);
    }, [selectedPhone]);

    async function handleConnect() {
        try {
            setConnecting(true);
            setError("");
            await startSession();
            setTimeout(async () => {
                try {
                    const qr = await getQrCode();
                    setQrCode(qr.qr_code_base64);
                } catch (e: any) {
                    setError(e?.response?.data?.message || "Falha ao buscar QR Code. Verifique se o WAHA está rodando (docker-compose).");
                } finally {
                    setConnecting(false);
                }
            }, 2000);
        } catch (e: any) {
            setError(e?.response?.data?.message || "Falha ao iniciar sessão. Verifique se o WAHA está rodando (docker-compose).");
            setConnecting(false);
        }
    }

    async function handleDisconnect() {
        await stopSession();
        setQrCode("");
        loadStatus();
    }

    async function handleSend() {
        if (!selectedPhone || !draft.trim()) return;
        try {
            setSending(true);
            await sendMessage(selectedPhone, draft.trim());
            setDraft("");
            await loadMessages(selectedPhone);
        } catch {
            setError("Falha ao enviar mensagem.");
        } finally {
            setSending(false);
        }
    }

    if (loading) {
        return <Box sx={{ display: "flex", justifyContent: "center", pt: 10 }}><CircularProgress sx={{ color: "#F97316" }} /></Box>;
    }

    const isConnected = status?.status === "WORKING" || status?.status === "connected";

    return (
        <Box>
            <Typography variant="h5" fontWeight="bold" color="#F8FAFC" gutterBottom>
                WhatsApp
            </Typography>
            <Typography variant="body2" color="#94A3B8" sx={{ mb: 3 }}>
                Conexão com o WhatsApp via WAHA (self-hosted). Escaneie o QR Code para conectar seu número.
            </Typography>

            {error && <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError("")}>{error}</Alert>}

            {status && !status.waha_reachable && (
                <Alert severity="warning" sx={{ mb: 3 }}>
                    O servidor WAHA não está acessível no momento. Ele precisa estar rodando (serviço <code>waha</code> no docker-compose)
                    para a conexão com o WhatsApp funcionar.
                </Alert>
            )}

            <Card sx={{ backgroundColor: "#0F172A", border: "1px solid #334155", mb: 3 }}>
                <CardContent sx={{ display: "flex", alignItems: "center", justifyContent: "space-between", flexWrap: "wrap", gap: 2 }}>
                    <Box>
                        <Typography color="#F8FAFC">
                            Status: <Chip
                                size="small"
                                label={status?.status || "desconhecido"}
                                sx={{
                                    ml: 1,
                                    backgroundColor: isConnected ? "#10B981" : "#334155",
                                    color: "#F8FAFC",
                                }}
                            />
                        </Typography>
                        {status?.phone_number && (
                            <Typography variant="body2" color="#94A3B8">Número: {status.phone_number}</Typography>
                        )}
                        {status?.last_error && (
                            <Typography variant="body2" color="#EF4444">{status.last_error}</Typography>
                        )}
                    </Box>

                    <Box sx={{ display: "flex", gap: 1 }}>
                        <Button
                            variant="contained"
                            startIcon={<QrCode2Icon />}
                            onClick={handleConnect}
                            disabled={connecting}
                            sx={{ backgroundColor: "#F97316", "&:hover": { backgroundColor: "#EA580C" } }}
                        >
                            {connecting ? "Gerando QR..." : "Conectar / Gerar QR Code"}
                        </Button>
                        <Button
                            variant="outlined"
                            startIcon={<PowerSettingsNewIcon />}
                            onClick={handleDisconnect}
                            sx={{ color: "#EF4444", borderColor: "#EF4444" }}
                        >
                            Desconectar
                        </Button>
                    </Box>
                </CardContent>
            </Card>

            {qrCode && (
                <Card sx={{ backgroundColor: "#0F172A", border: "1px solid #334155", mb: 3 }}>
                    <CardContent sx={{ display: "flex", flexDirection: "column", alignItems: "center" }}>
                        <Typography color="#94A3B8" sx={{ mb: 2 }}>Escaneie com o WhatsApp do celular:</Typography>
                        <img
                            src={qrCode.startsWith("data:") ? qrCode : `data:image/png;base64,${qrCode}`}
                            alt="QR Code WhatsApp"
                            style={{ width: 260, height: 260, background: "#fff", padding: 8, borderRadius: 8 }}
                        />
                    </CardContent>
                </Card>
            )}

            <Grid container spacing={2}>
                <Grid item xs={12} md={4}>
                    <Card sx={{ backgroundColor: "#0F172A", border: "1px solid #334155", height: 480, overflow: "auto" }}>
                        <CardContent>
                            <Typography variant="subtitle1" color="#F8FAFC" gutterBottom>Conversas</Typography>
                            {conversations.length === 0 && (
                                <Typography variant="body2" color="#64748B">Nenhuma conversa ainda.</Typography>
                            )}
                            <List>
                                {conversations.map((c) => (
                                    <ListItemButton
                                        key={c.contact_phone}
                                        selected={selectedPhone === c.contact_phone}
                                        onClick={() => setSelectedPhone(c.contact_phone)}
                                        sx={{
                                            borderRadius: 1,
                                            mb: 0.5,
                                            "&.Mui-selected": { backgroundColor: "#1E293B" },
                                        }}
                                    >
                                        <ListItemText
                                            primary={<Typography color="#F8FAFC">{c.contact_name || c.contact_phone}</Typography>}
                                            secondary={<Typography variant="body2" color="#94A3B8" noWrap>{c.last_message}</Typography>}
                                        />
                                    </ListItemButton>
                                ))}
                            </List>
                        </CardContent>
                    </Card>
                </Grid>

                <Grid item xs={12} md={8}>
                    <Card sx={{ backgroundColor: "#0F172A", border: "1px solid #334155", height: 480, display: "flex", flexDirection: "column" }}>
                        <CardContent sx={{ flex: 1, overflow: "auto" }}>
                            {!selectedPhone && (
                                <Typography variant="body2" color="#64748B">Selecione uma conversa para ver as mensagens.</Typography>
                            )}
                            {messages.map((m) => (
                                <Box
                                    key={m.id}
                                    sx={{
                                        display: "flex",
                                        justifyContent: m.direction === "out" ? "flex-end" : "flex-start",
                                        mb: 1,
                                    }}
                                >
                                    <Box
                                        sx={{
                                            maxWidth: "70%",
                                            backgroundColor: m.direction === "out" ? "#2563EB" : "#1E293B",
                                            color: "#F8FAFC",
                                            borderRadius: 2,
                                            px: 1.5,
                                            py: 1,
                                        }}
                                    >
                                        <Typography variant="body2">{m.body}</Typography>
                                        {m.is_from_agent && (
                                            <Typography variant="caption" color="#94A3B8">agente de IA</Typography>
                                        )}
                                    </Box>
                                </Box>
                            ))}
                        </CardContent>
                        <Divider sx={{ borderColor: "#334155" }} />
                        <Box sx={{ p: 2, display: "flex", gap: 1 }}>
                            <TextField
                                fullWidth
                                size="small"
                                placeholder="Digite uma mensagem..."
                                value={draft}
                                disabled={!selectedPhone}
                                onChange={(e) => setDraft(e.target.value)}
                                onKeyDown={(e) => { if (e.key === "Enter") handleSend(); }}
                                InputProps={{ sx: { color: "#F8FAFC" } }}
                            />
                            <Button
                                variant="contained"
                                startIcon={<SendIcon />}
                                onClick={handleSend}
                                disabled={!selectedPhone || sending}
                                sx={{ backgroundColor: "#F97316", "&:hover": { backgroundColor: "#EA580C" } }}
                            >
                                Enviar
                            </Button>
                        </Box>
                    </Card>
                </Grid>
            </Grid>
        </Box>
    );
}
