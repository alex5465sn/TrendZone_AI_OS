import type { ReactNode } from "react";

import { Box } from "@mui/material";

import Header from "./Header/Header";
import Sidebar from "./Sidebar/Sidebar";

interface DashboardLayoutProps {
    children: ReactNode;
}

export default function DashboardLayout({
    children,
}: DashboardLayoutProps) {
    return (
        <Box
            sx={{
                display: "flex",
                minHeight: "100vh",
                backgroundColor: "#0B1120",
            }}
        >
            <Sidebar />

            <Box
                sx={{
                    flex: 1,
                    display: "flex",
                    flexDirection: "column",
                    minWidth: 0,
                }}
            >
                <Header />

                <Box
                    sx={{
                        flex: 1,
                        p: 4,
                        overflow: "auto",
                    }}
                >
                    {children}
                </Box>
            </Box>
        </Box>
    );
}
