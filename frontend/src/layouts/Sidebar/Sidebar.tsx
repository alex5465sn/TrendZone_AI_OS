import {
    Box,
    List,
    ListItemButton,
    ListItemIcon,
    ListItemText,
    Typography,
} from "@mui/material";

import DashboardIcon from "@mui/icons-material/Dashboard";
import InventoryIcon from "@mui/icons-material/Inventory2";
import SmartToyIcon from "@mui/icons-material/SmartToy";
import AnalyticsIcon from "@mui/icons-material/Analytics";
import SettingsIcon from "@mui/icons-material/Settings";

import {
    NavLink,
} from "react-router-dom";

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
                width: 260,
                backgroundColor: "#111827",
                color: "#fff",
                display: "flex",
                flexDirection: "column",
                borderRight: "1px solid #1E293B",
            }}
        >

            <Typography
                variant="h6"
                fontWeight="bold"
                p={3}
            >

                Sistema operacional de IA da TrendZone

            </Typography>

            <List>

                {

                    menu.map((item) => (

                        <ListItemButton

                            key={item.path}

                            component={NavLink}

                            to={item.path}

                            sx={{

                                color: "#CBD5E1",

                                "&.active": {

                                    backgroundColor: "#2563EB",

                                    color: "#fff",

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

                            />

                        </ListItemButton>

                    ))

                }

            </List>

        </Box>

    );

}