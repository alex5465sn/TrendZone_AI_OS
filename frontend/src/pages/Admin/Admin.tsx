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
    CircularProgress,
    Alert,
    Chip,
    Button,
} from "@mui/material";

import PeopleIcon from "@mui/icons-material/People";
import InventoryIcon from "@mui/icons-material/Inventory2";
import AdminPanelSettingsIcon from "@mui/icons-material/AdminPanelSettings";
import StorageIcon from "@mui/icons-material/Storage";

import api from "../../api/axios";

interface AdminStats {
    total_users: number;
    total_products: number;
    total_admins: number;
    system_status: string;
}

interface User {
    id: number;
    uuid: string;
    name: string;
    email: string;
    role: string;
    plan: string;
    company: string;
    is_active: boolean;
    created_at: string;
}

export default function Admin() {

    const [stats, setStats] = useState<AdminStats | null>(null);
    const [users, setUsers] = useState<User[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    useEffect(() => {

        async function loadData() {

            try {

                setLoading(true);

                const [statsRes, usersRes] = await Promise.all([
                    api.get("/admin/stats"),
                    api.get("/admin/users"),
                ]);

                setStats(statsRes.data.data);
                setUsers(usersRes.data.data);

            } catch (err) {

                console.error(err);
                setError("Erro ao carregar dados administrativos.");

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

            <Typography
                variant="h4"
                fontWeight="bold"
                color="#F8FAFC"
                mb={4}
            >
                Painel Administrativo
            </Typography>

            <Grid container spacing={3} mb={4}>

                <Grid item xs={12} md={3}>
                    <Card sx={{ backgroundColor: "#111827", borderRadius: 3, border: "1px solid #1E293B" }}>
                        <CardContent>
                            <Box sx={{ display: "flex", alignItems: "center", gap: 2 }}>
                                <Box sx={{ p: 1.5, borderRadius: 2, backgroundColor: "#2563EB33", color: "#2563EB" }}>
                                    <PeopleIcon />
                                </Box>
                                <Box>
                                    <Typography color="#94A3B8" fontSize="0.875rem">Total de Usuários</Typography>
                                    <Typography variant="h5" fontWeight="bold" color="#F8FAFC">
                                        {stats?.total_users}
                                    </Typography>
                                </Box>
                            </Box>
                        </CardContent>
                    </Card>
                </Grid>

                <Grid item xs={12} md={3}>
                    <Card sx={{ backgroundColor: "#111827", borderRadius: 3, border: "1px solid #1E293B" }}>
                        <CardContent>
                            <Box sx={{ display: "flex", alignItems: "center", gap: 2 }}>
                                <Box sx={{ p: 1.5, borderRadius: 2, backgroundColor: "#10B98133", color: "#10B981" }}>
                                    <AdminPanelSettingsIcon />
                                </Box>
                                <Box>
                                    <Typography color="#94A3B8" fontSize="0.875rem">Administradores</Typography>
                                    <Typography variant="h5" fontWeight="bold" color="#F8FAFC">
                                        {stats?.total_admins}
                                    </Typography>
                                </Box>
                            </Box>
                        </CardContent>
                    </Card>
                </Grid>

                <Grid item xs={12} md={3}>
                    <Card sx={{ backgroundColor: "#111827", borderRadius: 3, border: "1px solid #1E293B" }}>
                        <CardContent>
                            <Box sx={{ display: "flex", alignItems: "center", gap: 2 }}>
                                <Box sx={{ p: 1.5, borderRadius: 2, backgroundColor: "#F59E0B33", color: "#F59E0B" }}>
                                    <InventoryIcon />
                                </Box>
                                <Box>
                                    <Typography color="#94A3B8" fontSize="0.875rem">Produtos</Typography>
                                    <Typography variant="h5" fontWeight="bold" color="#F8FAFC">
                                        {stats?.total_products}
                                    </Typography>
                                </Box>
                            </Box>
                        </CardContent>
                    </Card>
                </Grid>

                <Grid item xs={12} md={3}>
                    <Card sx={{ backgroundColor: "#111827", borderRadius: 3, border: "1px solid #1E293B" }}>
                        <CardContent>
                            <Box sx={{ display: "flex", alignItems: "center", gap: 2 }}>
                                <Box sx={{ p: 1.5, borderRadius: 2, backgroundColor: "#8B5CF633", color: "#8B5CF6" }}>
                                    <StorageIcon />
                                </Box>
                                <Box>
                                    <Typography color="#94A3B8" fontSize="0.875rem">Status</Typography>
                                    <Typography variant="h5" fontWeight="bold" color="#F8FAFC">
                                        {stats?.system_status === "online" ? "Online" : "Offline"}
                                    </Typography>
                                </Box>
                            </Box>
                        </CardContent>
                    </Card>
                </Grid>

            </Grid>

            <Card sx={{ backgroundColor: "#111827", borderRadius: 3, border: "1px solid #1E293B" }}>

                <CardContent>

                    <Typography variant="h6" fontWeight="bold" color="#F8FAFC" mb={3}>
                        Usuários do Sistema
                    </Typography>

                    <TableContainer>

                        <Table>

                            <TableHead>
                                <TableRow>
                                    <TableCell sx={{ color: "#94A3B8" }}>Nome</TableCell>
                                    <TableCell sx={{ color: "#94A3B8" }}>Email</TableCell>
                                    <TableCell sx={{ color: "#94A3B8" }}>Role</TableCell>
                                    <TableCell sx={{ color: "#94A3B8" }}>Plano</TableCell>
                                    <TableCell sx={{ color: "#94A3B8" }}>Status</TableCell>
                                    <TableCell sx={{ color: "#94A3B8" }}>Ações</TableCell>
                                </TableRow>
                            </TableHead>

                            <TableBody>

                                {users.map((user) => (

                                    <TableRow key={user.id} hover>

                                        <TableCell sx={{ color: "#F8FAFC" }}>{user.name}</TableCell>

                                        <TableCell sx={{ color: "#94A3B8" }}>{user.email}</TableCell>

                                        <TableCell>
                                            <Chip
                                                label={user.role}
                                                color={user.role === "ADMIN" ? "error" : "default"}
                                                size="small"
                                                sx={{ fontWeight: 600 }}
                                            />
                                        </TableCell>

                                        <TableCell sx={{ color: "#F8FAFC" }}>{user.plan}</TableCell>

                                        <TableCell>
                                            <Chip
                                                label={user.is_active ? "Ativo" : "Inativo"}
                                                color={user.is_active ? "success" : "default"}
                                                size="small"
                                            />
                                        </TableCell>

                                        <TableCell>
                                            <Button size="small" sx={{ color: "#38BDF8" }}>
                                                Editar
                                            </Button>
                                        </TableCell>

                                    </TableRow>

                                ))}

                            </TableBody>

                        </Table>

                    </TableContainer>

                </CardContent>

            </Card>

        </Box>

    );

}
