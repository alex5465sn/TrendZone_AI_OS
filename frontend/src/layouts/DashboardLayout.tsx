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
                backgroundColor: "#0F172A",
            }}
        >
            <Sidebar />

            <Box
                sx={{
                    flex: 1,
                    display: "flex",
                    flexDirection: "column",
                }}
            >
                <Header />

                <Box
                    sx={{
                        flex: 1,
                        p: 4,
                    }}
                >
                    {children}
                </Box>
            </Box>
        </Box>
    );
}