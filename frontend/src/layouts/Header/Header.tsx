import {
    AppBar,
    Toolbar,
    Typography,
    Box,
    Avatar,
    TextField
} from "@mui/material";

export default function Header() {

    return (

        <AppBar
            position="static"
            elevation={0}
            sx={{
                bgcolor:"#0F172A",
                borderBottom:"1px solid #1E293B"
            }}
        >

            <Toolbar>

                <Typography
                    variant="h5"
                    fontWeight="bold"
                >

                    TrendZone AI OS

                </Typography>

                <Box sx={{flex:1}} />

                <TextField
                    size="small"
                    placeholder="Pesquisar..."
                    sx={{
                        width:300,
                        mr:3,
                        bgcolor:"#FFF",
                        borderRadius:1
                    }}
                />

                <Avatar>

                    A

                </Avatar>

            </Toolbar>

        </AppBar>

    );

}