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
import CampaignIcon from "@mui/icons-material/Campaign";
import TravelExploreIcon from "@mui/icons-material/TravelExplore";
import AttachMoneyIcon from "@mui/icons-material/AttachMoney";
import BugReportIcon from "@mui/icons-material/BugReport";
import LinkIcon from "@mui/icons-material/Link";
import AdminPanelSettingsIcon from "@mui/icons-material/AdminPanelSettings";
import ViewKanbanIcon from "@mui/icons-material/ViewKanban";
import RocketLaunchIcon from "@mui/icons-material/RocketLaunch";
import AutoAwesomeIcon from "@mui/icons-material/AutoAwesome";
import NotificationsActiveIcon from "@mui/icons-material/NotificationsActive";
import HubIcon from "@mui/icons-material/Hub";
import CalendarMonthIcon from "@mui/icons-material/CalendarMonth";
import BoltIcon from "@mui/icons-material/Bolt";
import HistoryIcon from "@mui/icons-material/History";
import TranslateIcon from "@mui/icons-material/Translate";
import WhatsAppIcon from "@mui/icons-material/WhatsApp";
import PsychologyIcon from "@mui/icons-material/Psychology";

import { NavLink } from "react-router-dom";
import { isAdmin } from "../../services/authService";

const baseMenu = [

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
        text: "Oportunidades",
        icon: <CampaignIcon />,
        path: "/opportunities",
    },

    {
        text: "Prospecção",
        icon: <TravelExploreIcon />,
        path: "/prospects",
    },

    {
        text: "Vendas & Comissões",
        icon: <AttachMoneyIcon />,
        path: "/sales",
    },

    {
        text: "Contas de Afiliado",
        icon: <LinkIcon />,
        path: "/accounts",
    },

    {
        text: "Funil de Vendas",
        icon: <ViewKanbanIcon />,
        path: "/funnel",
    },

    {
        text: "Descoberta",
        icon: <RocketLaunchIcon />,
        path: "/discovery",
    },

    {
        text: "Conteúdo IA",
        icon: <AutoAwesomeIcon />,
        path: "/content-strategy",
    },

    {
        text: "Follow-ups",
        icon: <NotificationsActiveIcon />,
        path: "/follow-ups",
    },

    {
        text: "Canais & SubIDs",
        icon: <HubIcon />,
        path: "/channels",
    },

    {
        text: "Calendário Sazonal",
        icon: <CalendarMonthIcon />,
        path: "/seasonal",
    },

    {
        text: "Automações",
        icon: <BoltIcon />,
        path: "/automation",
    },

    {
        text: "Log de Auditoria",
        icon: <HistoryIcon />,
        path: "/audit-log",
    },

    {
        text: "Vocabulário",
        icon: <TranslateIcon />,
        path: "/vocabulary",
    },

    {
        text: "WhatsApp",
        icon: <WhatsAppIcon />,
        path: "/whatsapp",
    },

    {
        text: "Agente de IA",
        icon: <PsychologyIcon />,
        path: "/ai-agent",
    },

    {
        text: "Inspetor",
        icon: <BugReportIcon />,
        path: "/inspector",
    },

    {
        text: "Configurações",
        icon: <SettingsIcon />,
        path: "/settings",
    },
];

const adminMenu = [
    {
        text: "Admin",
        icon: <AdminPanelSettingsIcon />,
        path: "/admin",
    },
];

const menu = isAdmin() ? [...baseMenu, ...adminMenu] : baseMenu;

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

                <Box
                    component="img"
                    src="/brand/logo.png"
                    alt="TrendZone AI OS"
                    sx={{
                        width: 44,
                        height: 44,
                        borderRadius: "50%",
                        objectFit: "cover",
                        boxShadow: "0 0 12px rgba(249,115,22,0.5)",
                    }}
                />

                <Box>

                    <Typography
                        variant="h6"
                        fontWeight="bold"
                        sx={{ fontSize: "1.1rem", lineHeight: 1.2 }}
                    >
                        TrendZone<Box component="span" sx={{ color: "#F97316" }}>AI</Box>
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
