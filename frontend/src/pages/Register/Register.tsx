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

import PersonAddIcon from "@mui/icons-material/PersonAdd";

import { register } from "../../services/authService";

export default function Register() {

    const navigate = useNavigate();

    const [name, setName] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [company, setCompany] = useState("");
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    async function handleRegister() {

        if (!name || !email || !password) {
            setError("Nome, email e senha são obrigatórios.");
            return;
        }

        if (password.length < 6) {
            setError("Senha deve ter no mínimo 6 caracteres.");
            return;
        }

        try {

            setLoading(true);
            setError("");

            await register({
                name,
                email,
                password,
                company,
            });

            navigate("/login");

        } catch (err: any) {

            console.error(err);
            setError(err.response?.data?.detail || "Erro ao registrar.");

        } finally {

            setLoading(false);

        }

    }

    function handleKeyPress(e: React.KeyboardEvent) {

        if (e.key === "Enter") {
            handleRegister();
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
                                    backgroundColor: "#8B5CF6",
                                    color: "#fff",
                                    display: "flex",
                                    alignItems: "center",
                                    justifyContent: "center",
                                }}
                            >

                                <PersonAddIcon sx={{ fontSize: 32 }} />

                            </Box>

                        </Box>

                        <Typography
                            variant="h4"
                            fontWeight="bold"
                            color="#F8FAFC"
                            textAlign="center"
                            mb={1}
                        >
                            Criar Conta
                        </Typography>

                        <Typography
                            variant="body2"
                            color="#94A3B8"
                            textAlign="center"
                            mb={4}
                        >
                            Junte-se ao TrendZone AI
                        </Typography>

                        {error && (
                            <Alert severity="error" sx={{ mb: 3 }}>
                                {error}
                            </Alert>
                        )}

                        <TextField
                            fullWidth
                            label="Nome Completo"
                            value={name}
                            onChange={(e) => setName(e.target.value)}
                            disabled={loading}
                            sx={{
                                mb: 2,
                                backgroundColor: "#0B1120",
                                borderRadius: 1,
                            }}
                        />

                        <TextField
                            fullWidth
                            label="Email"
                            type="email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            disabled={loading}
                            sx={{
                                mb: 2,
                                backgroundColor: "#0B1120",
                                borderRadius: 1,
                            }}
                        />

                        <TextField
                            fullWidth
                            label="Empresa (opcional)"
                            value={company}
                            onChange={(e) => setCompany(e.target.value)}
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
                            onClick={handleRegister}
                            disabled={loading}
                            sx={{
                                backgroundColor: "#8B5CF6",
                                py: 1.5,
                                mb: 2,
                                textTransform: "none",
                                fontSize: "1rem",
                                fontWeight: 600,
                            }}
                        >
                            {loading ? <CircularProgress size={24} color="inherit" /> : "Registrar"}
                        </Button>

                        <Box sx={{ textAlign: "center" }}>

                            <Typography variant="body2" color="#94A3B8">
                                Já tem conta?{" "}
                                <Link
                                    href="/login"
                                    sx={{
                                        color: "#38BDF8",
                                        textDecoration: "none",
                                        fontWeight: 600,
                                        "&:hover": {
                                            textDecoration: "underline",
                                        },
                                    }}
                                >
                                    Faça login
                                </Link>
                            </Typography>

                        </Box>

                    </CardContent>

                </Card>

            </Container>

        </Box>

    );

}
