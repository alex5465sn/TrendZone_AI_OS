import { useState } from "react";
import { useNavigate } from "react-router-dom";

import {
    Box,
    Container,
    TextField,
    Button,
    Typography,
    Alert,
    CircularProgress,
    Card,
    CardContent,
    Link,
} from "@mui/material";

import LockIcon from "@mui/icons-material/Lock";

import { login } from "../../services/authService";

export default function Login() {

    const navigate = useNavigate();

    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    async function handleLogin() {

        if (!email || !password) {
            setError("Email e senha são obrigatórios.");
            return;
        }

        try {

            setLoading(true);
            setError("");

            await login({
                email,
                password,
            });

            navigate("/dashboard");

        } catch (err: any) {

            console.error(err);
            setError(err.response?.data?.detail || "Erro ao fazer login.");

        } finally {

            setLoading(false);

        }

    }

    function handleKeyPress(e: React.KeyboardEvent) {

        if (e.key === "Enter") {
            handleLogin();
        }

    }

    return (

        <Box
            sx={{
                minHeight: "100vh",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                background: "linear-gradient(135deg, #0B1120 0%, #1E293B 100%)",
            }}
        >

            <Container maxWidth="sm">

                <Card
                    sx={{
                        backgroundColor: "#111827",
                        border: "1px solid #1E293B",
                        borderRadius: 3,
                    }}
                >

                    <CardContent sx={{ p: 4 }}>

                        <Box
                            sx={{
                                display: "flex",
                                justifyContent: "center",
                                mb: 3,
                            }}
                        >

                            <Box
                                sx={{
                                    p: 2,
                                    borderRadius: 2,
                                    backgroundColor: "#2563EB",
                                    color: "#fff",
                                    display: "flex",
                                    alignItems: "center",
                                    justifyContent: "center",
                                }}
                            >

                                <LockIcon sx={{ fontSize: 32 }} />

                            </Box>

                        </Box>

                        <Typography
                            variant="h4"
                            fontWeight="bold"
                            color="#F8FAFC"
                            textAlign="center"
                            mb={1}
                        >
                            TrendZone AI
                        </Typography>

                        <Typography
                            variant="body2"
                            color="#94A3B8"
                            textAlign="center"
                            mb={4}
                        >
                            Sistema Operacional de IA para Afiliados
                        </Typography>

                        {error && (
                            <Alert severity="error" sx={{ mb: 3 }}>
                                {error}
                            </Alert>
                        )}

                        <TextField
                            fullWidth
                            label="Email"
                            type="email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            onKeyPress={handleKeyPress}
                            disabled={loading}
                            sx={{
                                mb: 2,
                                backgroundColor: "#0B1120",
                                borderRadius: 1,
                            }}
                        />

                        <TextField
                            fullWidth
                            label="Senha"
                            type="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            onKeyPress={handleKeyPress}
                            disabled={loading}
                            sx={{
                                mb: 3,
                                backgroundColor: "#0B1120",
                                borderRadius: 1,
                            }}
                        />

                        <Button
                            fullWidth
                            variant="contained"
                            onClick={handleLogin}
                            disabled={loading}
                            sx={{
                                backgroundColor: "#2563EB",
                                py: 1.5,
                                mb: 2,
                                textTransform: "none",
                                fontSize: "1rem",
                                fontWeight: 600,
                            }}
                        >
                            {loading ? <CircularProgress size={24} color="inherit" /> : "Entrar"}
                        </Button>

                        <Box sx={{ textAlign: "center" }}>

                            <Typography variant="body2" color="#94A3B8">
                                Não tem conta?{" "}
                                <Link
                                    href="/register"
                                    sx={{
                                        color: "#38BDF8",
                                        textDecoration: "none",
                                        fontWeight: 600,
                                        "&:hover": {
                                            textDecoration: "underline",
                                        },
                                    }}
                                >
                                    Registre-se
                                </Link>
                            </Typography>

                        </Box>

                    </CardContent>

                </Card>

            </Container>

        </Box>

    );

}
