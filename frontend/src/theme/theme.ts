import { createTheme } from "@mui/material/styles";

const theme = createTheme({
    palette: {
        mode: "dark",

        primary: {
            main: "#2563EB",
            light: "#3B82F6",
            dark: "#1D4ED8",
            contrastText: "#FFFFFF",
        },

        secondary: {
            main: "#8B5CF6",
            light: "#A78BFA",
            dark: "#7C3AED",
            contrastText: "#FFFFFF",
        },

        background: {
            default: "#0B1120",
            paper: "#111827",
        },

        success: {
            main: "#10B981",
            light: "#34D399",
            dark: "#059669",
        },

        warning: {
            main: "#F59E0B",
            light: "#FBBF24",
            dark: "#D97706",
        },

        error: {
            main: "#EF4444",
            light: "#F87171",
            dark: "#DC2626",
        },

        info: {
            main: "#38BDF8",
            light: "#7DD3FC",
            dark: "#0284C7",
        },

        text: {
            primary: "#F8FAFC",
            secondary: "#94A3B8",
            disabled: "#64748B",
        },
    },

    shape: {
        borderRadius: 12,
    },

    typography: {
        fontFamily: "Inter, Roboto, sans-serif",

        h4: {
            fontWeight: 700,
        },

        h5: {
            fontWeight: 600,
        },

        h6: {
            fontWeight: 600,
        },

        button: {
            textTransform: "none",
            fontWeight: 600,
        },
    },

    components: {
        MuiCssBaseline: {
            styleOverrides: {
                body: {
                    backgroundColor: "#0B1120",
                    color: "#F8FAFC",
                },
            },
        },

        MuiCard: {
            styleOverrides: {
                root: {
                    boxShadow: "none",
                    border: "1px solid #1E293B",
                },
            },
        },

        MuiButton: {
            styleOverrides: {
                root: {
                    borderRadius: 10,
                },
            },
        },

        MuiTextField: {
            styleOverrides: {
                root: {
                    "& .MuiOutlinedInput-root": {
                        borderRadius: 10,
                        backgroundColor: "#111827",
                        "& fieldset": {
                            borderColor: "#1E293B",
                        },
                        "&:hover fieldset": {
                            borderColor: "#3B82F6",
                        },
                        "&.Mui-focused fieldset": {
                            borderColor: "#2563EB",
                        },
                    },
                    "& .MuiInputLabel-root": {
                        color: "#94A3B8",
                    },
                },
            },
        },
    },
});

export default theme;
