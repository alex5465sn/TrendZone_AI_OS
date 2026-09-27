import {
    AppBar,
    Toolbar,
    Typography,
    Box,
    Avatar,
    IconButton,
    Badge,
    Tooltip,
} from "@mui/material";

import NotificationsIcon from "@mui/icons-material/Notifications";
import SettingsIcon from "@mui/icons-material/Settings";
import LogoutIcon from "@mui/icons-material/Logout";
import NotificationBell from "../../components/NotificationBell/NotificationBell";
import { useNavigate } from "react-router-dom";

import { logout, getUserInfo } from "../../services/authService";

export default function Header() {

    const navigate = useNavigate();
    const user = getUserInfo();

    async function handleLogout() {
        if (!window.confirm("Deseja encerrar a sessão?")) return;
        await logout();
        navigate("/login", { replace: true });
    }

    return (

        <AppBar
            position="static"
            elevation={0}
            sx={{
                bgcolor: "#0B1120",
                borderBottom: "1px solid #1E293B",
            }}
        >

            <Toolbar>

                <Typography
                    variant="h6"
                    fontWeight="bold"
                    color="#F8FAFC"
                >
                    TrendZone AI OS
                </Typography>

                <Box sx={{ flex: 1 }} />

                <NotificationBell />

                <Tooltip title="Configurações">
                    <IconButton
                        size="large"
                        sx={{ color: "#94A3B8", mr: 1 }}
                        onClick={() => navigate("/settings")}
                    >
                        <SettingsIcon />
                    </IconButton>
                </Tooltip>

                <Tooltip title="Encerrar sessão">
                    <IconButton
                        size="large"
                        sx={{ color: "#94A3B8", mr: 2 }}
                        onClick={handleLogout}
                    >
                        <LogoutIcon />
                    </IconButton>
                </Tooltip>

                <Box
                    sx={{
                        display: "flex",
                        alignItems: "center",
                        gap: 1.5,
                    }}
                >

                    <Avatar
                        sx={{
                            bgcolor: "#2563EB",
                            width: 36,
                            height: 36,
                        }}
                    >
                        A
                    </Avatar>

                    <Box sx={{ display: { xs: "none", md: "block" } }}>

                        <Typography
                            variant="body2"
                            fontWeight="bold"
                            color="#F8FAFC"
                            lineHeight={1.2}
                        >
                            {user?.name || user?.email || "Usuário"}
                        </Typography>

                        <Typography
                            variant="caption"
                            color="#94A3B8"
                        >
                            {user?.role === "admin" ? "Administrador" : "Afiliado"}
                        </Typography>

                    </Box>

                </Box>

            </Toolbar>

        </AppBar>

    );

}
