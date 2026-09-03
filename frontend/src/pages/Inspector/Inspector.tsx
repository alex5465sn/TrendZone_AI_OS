import { useState } from "react";

import {
    Box,
    Typography,
    Grid,
    Card,
    CardContent,
    Button,
    CircularProgress,
    Snackbar,
    Chip,
    Divider,
    List,
    ListItem,
    ListItemIcon,
    ListItemText,
} from "@mui/material";

import BugReportIcon from "@mui/icons-material/BugReport";
import CheckCircleIcon from "@mui/icons-material/CheckCircle";
import ErrorIcon from "@mui/icons-material/Error";
import WarningIcon from "@mui/icons-material/Warning";
import InfoIcon from "@mui/icons-material/Info";
import PlayArrowIcon from "@mui/icons-material/PlayArrow";

import {
    runFullInspection,
    type InspectionReport,
    type InspectionResult,
} from "../../services/inspectorService";

function severityIcon(severity: string) {
    if (severity === "error") return <ErrorIcon sx={{ color: "#EF4444" }} />;
    if (severity === "warning") return <WarningIcon sx={{ color: "#F59E0B" }} />;
    return <InfoIcon sx={{ color: "#38BDF8" }} />;
}

function severityColor(severity: string) {
    if (severity === "error") return "#EF4444";
    if (severity === "warning") return "#F59E0B";
    return "#38BDF8";
}

export default function Inspector() {

    const [report, setReport] = useState<InspectionReport | null>(null);
    const [loading, setLoading] = useState(false);
    const [toast, setToast] = useState("");

    async function handleInspect() {
        try {
            setLoading(true);
            const data = await runFullInspection();
            setReport(data);
            if (data.errors === 0 && data.warnings === 0) {
                setToast("Inspecao concluida: nenhum problema encontrado!");
            } else {
                setToast(`Inspecao concluida: ${data.errors} erro(s), ${data.warnings} aviso(s).`);
            }
        } catch {
            setToast("Erro ao executar inspecao. Verifique se voce tem permissao de Admin.");
        } finally {
            setLoading(false);
        }
    }

    const cardSx = { backgroundColor: "#111827", borderRadius: 3, border: "1px solid #1E293B" };

    return (

        <Box>

            <Box sx={{ display: "flex", alignItems: "center", gap: 1.5, mb: 1 }}>
                <BugReportIcon sx={{ color: "#8B5CF6" }} />
                <Typography variant="h4" fontWeight="bold" color="#F8FAFC">
                    Inspetor da Plataforma
                </Typography>
            </Box>

            <Typography color="#94A3B8" mb={3}>
                Varre automaticamente o codigo, imports, banco de dados, logs e configuracoes
                da plataforma. Detecta problemas e reporta com arquivo, linha e severidade.
            </Typography>

            <Button
                variant="contained"
                size="large"
                startIcon={loading ? <CircularProgress size={20} /> : <PlayArrowIcon />}
                onClick={handleInspect}
                disabled={loading}
                sx={{ mb: 4, backgroundColor: "#8B5CF6", "&:hover": { backgroundColor: "#7C3AED" } }}
            >
                {loading ? "Inspecionando..." : "Executar Inspecao Completa"}
            </Button>

            {report && (
                <>
                    <Grid container spacing={3} sx={{ mb: 4 }}>
                        <Grid item xs={6} sm={3}>
                            <Card sx={cardSx}>
                                <CardContent sx={{ textAlign: "center" }}>
                                    <Typography variant="caption" color="#94A3B8">Status</Typography>
                                    <Box sx={{ mt: 1 }}>
                                        {report.errors === 0 ? (
                                            <CheckCircleIcon sx={{ fontSize: 40, color: "#10B981" }} />
                                        ) : (
                                            <ErrorIcon sx={{ fontSize: 40, color: "#EF4444" }} />
                                        )}
                                    </Box>
                                    <Typography fontWeight="bold" color={report.errors === 0 ? "#10B981" : "#EF4444"}>
                                        {report.status}
                                    </Typography>
                                </CardContent>
                            </Card>
                        </Grid>
                        <Grid item xs={6} sm={3}>
                            <Card sx={cardSx}>
                                <CardContent sx={{ textAlign: "center" }}>
                                    <Typography variant="caption" color="#94A3B8">Erros</Typography>
                                    <Typography variant="h3" fontWeight="bold" color="#EF4444">
                                        {report.errors}
                                    </Typography>
                                </CardContent>
                            </Card>
                        </Grid>
                        <Grid item xs={6} sm={3}>
                            <Card sx={cardSx}>
                                <CardContent sx={{ textAlign: "center" }}>
                                    <Typography variant="caption" color="#94A3B8">Avisos</Typography>
                                    <Typography variant="h3" fontWeight="bold" color="#F59E0B">
                                        {report.warnings}
                                    </Typography>
                                </CardContent>
                            </Card>
                        </Grid>
                        <Grid item xs={6} sm={3}>
                            <Card sx={cardSx}>
                                <CardContent sx={{ textAlign: "center" }}>
                                    <Typography variant="caption" color="#94A3B8">Verificacoes</Typography>
                                    <Typography variant="h3" fontWeight="bold" color="#38BDF8">
                                        {report.total_checks}
                                    </Typography>
                                </CardContent>
                            </Card>
                        </Grid>
                    </Grid>

                    <Divider sx={{ borderColor: "#1E293B", mb: 3 }} />

                    <Typography variant="h6" color="#F8FAFC" mb={2}>
                        Relatorio Detalhado
                    </Typography>

                    <Card sx={cardSx}>
                        <List dense>
                            {report.results.map((r: InspectionResult, idx: number) => (
                                <ListItem
                                    key={idx}
                                    sx={{ borderBottom: "1px solid #1E293B" }}
                                >
                                    <ListItemIcon sx={{ minWidth: 36 }}>
                                        {severityIcon(r.severity)}
                                    </ListItemIcon>
                                    <ListItemText
                                        primary={
                                            <Box sx={{ display: "flex", alignItems: "center", gap: 1, flexWrap: "wrap" }}>
                                                <Chip
                                                    label={r.severity.toUpperCase()}
                                                    size="small"
                                                    sx={{
                                                        backgroundColor: severityColor(r.severity),
                                                        color: "#0B1120",
                                                        fontWeight: 700,
                                                        fontSize: "0.7rem",
                                                    }}
                                                />
                                                <Typography variant="body2" color="#F8FAFC" component="span" sx={{ fontFamily: "monospace" }}>
                                                    {r.file}{r.line > 0 ? `:${r.line}` : ""}
                                                </Typography>
                                                {r.fixed && (
                                                    <Chip
                                                        label="CORRIGIDO"
                                                        size="small"
                                                        sx={{ backgroundColor: "#10B981", color: "#0B1120", fontWeight: 700, fontSize: "0.65rem" }}
                                                    />
                                                )}
                                            </Box>
                                        }
                                        secondary={
                                            <Typography variant="body2" color="#94A3B8" sx={{ mt: 0.5 }}>
                                                {r.message}
                                                {r.fix_detail ? ` — ${r.fix_detail}` : ""}
                                            </Typography>
                                        }
                                    />
                                </ListItem>
                            ))}
                        </List>
                    </Card>
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
