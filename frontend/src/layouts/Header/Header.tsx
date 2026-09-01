import {
    AppBar,
    Toolbar,
    Typography,
    Box,
    Avatar,
    IconButton,
    Badge,
} from "@mui/material";

import NotificationsIcon from "@mui/icons-material/Notifications";
import SettingsIcon from "@mui/icons-material/Settings";

export default function Header() {

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

                <IconButton
                    size="large"
                    sx={{ color: "#94A3B8", mr: 1 }}
                >
                    <Badge badgeContent={0} color="error">
                        <NotificationsIcon />
                    </Badge>
                </IconButton>

                <IconButton
                    size="large"
                    sx={{ color: "#94A3B8", mr: 2 }}
                >
                    <SettingsIcon />
                </IconButton>

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

            </Toolbar>

        </AppBar>

    );

}
