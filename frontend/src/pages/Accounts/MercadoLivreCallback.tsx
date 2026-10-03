import { useEffect, useState } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import {
    Box,
    Button,
    CircularProgress,
    Paper,
    Typography,
} from "@mui/material";
import { CheckCircle, ErrorOutline } from "@mui/icons-material";

import { getData } from "../../services/apiResponse";

export default function MercadoLivreCallback() {
    const [searchParams] = useSearchParams();
    const navigate = useNavigate();
    const [status, setStatus] = useState<"loading" | "success" | "error">(
        "loading"
    );
    const [message, setMessage] = useState("");

    useEffect(() => {
        const code = searchParams.get("code");
        const state = searchParams.get("state") || "";
        const authError = searchParams.get("error");

        if (authError) {
            setStatus("error");
            setMessage(
                searchParams.get("error_description") ||
                    "O Mercado Livre não autorizou a conexão."
            );
            return;
        }

        if (!code) {
            setStatus("error");
            setMessage("Código de autorização não encontrado na URL.");
            return;
        }

        getData(
            `/mercadolivre/callback?code=${encodeURIComponent(code)}&state=${encodeURIComponent(
                state
            )}`
        )
            .then(() => {
                setStatus("success");
            })
            .catch((e: unknown) => {
                setStatus("error");
                setMessage(
                    e instanceof Error
                        ? e.message
                        : "Falha ao concluir a conexão com o Mercado Livre."
                );
            });
    }, [searchParams]);

    return (
        <Box
            display="flex"
            justifyContent="center"
            alignItems="center"
            minHeight="80vh"
        >
            <Paper
                sx={{
                    p: 4,
                    maxWidth: 420,
                    textAlign: "center",
                    backgroundColor: "#111827",
                }}
            >
                {status === "loading" && (
                    <>
                        <CircularProgress sx={{ mb: 2 }} />
                        <Typography color="#F8FAFC">
                            Concluindo a conexão com o Mercado Livre...
                        </Typography>
                    </>
                )}

                {status === "success" && (
                    <>
                        <CheckCircle
                            sx={{ fontSize: 48, color: "#10B981", mb: 2 }}
                        />
                        <Typography
                            variant="h6"
                            fontWeight={700}
                            color="#F8FAFC"
                            mb={1}
                        >
                            Conta conectada!
                        </Typography>
                        <Typography color="#94A3B8" mb={3}>
                            Sua conta do Mercado Livre foi autorizada e
                            conectada com sucesso.
                        </Typography>
                        <Button
                            variant="contained"
                            onClick={() => navigate("/accounts")}
                        >
                            Voltar para Contas
                        </Button>
                    </>
                )}

                {status === "error" && (
                    <>
                        <ErrorOutline
                            sx={{ fontSize: 48, color: "#F59E0B", mb: 2 }}
                        />
                        <Typography
                            variant="h6"
                            fontWeight={700}
                            color="#F8FAFC"
                            mb={1}
                        >
                            Não foi possível conectar
                        </Typography>
                        <Typography color="#94A3B8" mb={3}>
                            {message}
                        </Typography>
                        <Button
                            variant="contained"
                            onClick={() => navigate("/accounts")}
                        >
                            Voltar para Contas
                        </Button>
                    </>
                )}
            </Paper>
        </Box>
    );
}
