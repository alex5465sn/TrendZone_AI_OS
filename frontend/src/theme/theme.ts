import { createTheme } from "@mui/material/styles";

const theme = createTheme({
    palette: {
        mode: "dark",

        primary: {
            main: "#38BDF8",
        },

        secondary: {
            main: "#8B5CF6",
        },

        background: {
            default: "#0B1220",
            paper: "#111827",
        },

        success: {
            main: "#10B981",
        },

        error: {
            main: "#EF4444",
        },

        text: {
            primary: "#F8FAFC",
            secondary: "#94A3B8",
        },
    },

    shape: {
        borderRadius: 14,
    },

    typography: {
        fontFamily: "Inter, sans-serif",

        h4: {
            fontWeight: 700,
        },

        h5: {
            fontWeight: 600,
        },

        button: {
            textTransform: "none",
            fontWeight: 600,
        },
    },
});

export default theme;