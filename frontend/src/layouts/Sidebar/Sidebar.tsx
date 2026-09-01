import {
    Box,
    List,
    ListItemButton,
    ListItemIcon,
    ListItemText,
    Typography,
    Avatar,
    Divider,
} from "@mui/material";

import DashboardIcon from "@mui/icons-material/Dashboard";
import InventoryIcon from "@mui/icons-material/Inventory2";
import SmartToyIcon from "@mui/icons-material/SmartToy";
import AnalyticsIcon from "@mui/icons-material/Analytics";
import SettingsIcon from "@mui/icons-material/Settings";
import TrendingUpIcon from "@mui/icons-material/TrendingUp";

import { NavLink } from "react-router-dom";

const menu = [

    {
        text: "Painel",
        icon: <DashboardIcon />,
        path: "/dashboard",
    },

    {
        text: "Produtos",
        icon: <InventoryIcon />,
        path: "/products",
    },

    {
        text: "Scout IA",
        icon: <SmartToyIcon />,
        path: "/scout",
    },

    {
        text: "Análises",
        icon: <AnalyticsIcon />,
        path: "/analytics",
    },

    {
        text: "Configurações",
        icon: <SettingsIcon />,
        path: "/settings",
    },

];

export default function Sidebar() {

    return (

        <Box
            sx={{
                width: 280,
                backgroundColor: "#0B1120",
                color: "#fff",
                display: "flex",
                flexDirection: "column",
                borderRight: "1px solid #1E293B",
                minHeight: "100vh",
            }}
        >

            <Box
                sx={{
                    p: 3,
                    display: "flex",
                    alignItems: "center",
                    gap: 2,
                }}
            >

                <Avatar
                    sx={{
                        backgroundColor: "#2563EB",
                        width: 40,
                        height: 40,
                    }}
                >
                    <TrendingUpIcon />
                </Avatar>

                <Box>

                    <Typography
                        variant="h6"
                        fontWeight="bold"
                        sx={{ fontSize: "1.1rem", lineHeight: 1.2 }}
                    >
                        TrendZone AI
                    </Typography>

                    <Typography
                        variant="caption"
                        color="#94A3B8"
                    >
                        Sistema Operacional de IA
                    </Typography>

                </Box>

            </Box>

            <Divider sx={{ borderColor: "#1E293B", mx: 2 }} />

            <Box
                sx={{
                    p: 3,
                    display: "flex",
                    alignItems: "center",
                    gap: 2,
                }}
            >

                <Avatar
                    src="/assets/avatar.png"
                    alt="Usuário"
                >
                    A
                </Avatar>

                <Box>

                    <Typography
                        variant="body2"
                        fontWeight="bold"
                        color="#F8FAFC"
                    >
                        Admin
                    </Typography>

                    <Typography
                        variant="caption"
                        color="#94A3B8"
                    >
                        Afiliado Shopee
                    </Typography>

                </Box>

            </Box>

            <Divider sx={{ borderColor: "#1E293B", mx: 2 }} />

            <Typography
                variant="caption"
                color="#64748B"
                sx={{
                    px: 3,
                    pt: 2,
                    pb: 1,
                    fontWeight: 600,
                    letterSpacing: 1,
                    textTransform: "uppercase",
                }}
            >
                Navegação
            </Typography>

            <List sx={{ px: 2 }}>

                {

                    menu.map((item) => (

                        <ListItemButton

                            key={item.path}
                            component={NavLink}
                            to={item.path}
                            sx={{
                                borderRadius: 2,
                                mb: 0.5,
                                color: "#94A3B8",
                                transition: "all 0.2s",
                                "&.active": {
                                    backgroundColor: "#2563EB",
                                    color: "#fff",
                                    boxShadow: "0 4px 14px rgba(37, 99, 235, 0.4)",
                                },
                                "&:hover": {
                                    backgroundColor: "#1E293B",
                                    color: "#F8FAFC",
                                },
                                "& .MuiListItemIcon-root": {
                                    color: "inherit",
                                },
                            }}

                        >

                            <ListItemIcon>
                                {item.icon}
                            </ListItemIcon>

                            <ListItemText
                                primary={item.text}
                                primaryTypographyProps={{
                                    fontWeight: 500,
                                }}
                            />

                        </ListItemButton>

                    ))

                }

            </List>

        </Box>

    );

}
