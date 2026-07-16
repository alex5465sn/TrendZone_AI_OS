import { useEffect, useState } from "react";

import {
    Box,
    Grid,
    Typography,
} from "@mui/material";

import StatCard from "../../components/dashboard/StatCard";
import HealthCard from "../../components/health/HealthCard";

import {
    getDashboard,
} from "../../services/dashboardService";

import type {
    DashboardData,
} from "../../services/dashboardService";

import {
    getHealth,
} from "../../services/healthService";

import type {
    HealthData,
} from "../../services/healthService";

export default function Dashboard() {

    const [dashboard, setDashboard] = useState<DashboardData | null>(null);
    const [health, setHealth] = useState<HealthData | null>(null);

    useEffect(() => {

        async function loadData() {

            try {

                const dashboardData = await getDashboard();
                const healthData = await getHealth();

                setDashboard(dashboardData);
                setHealth(healthData);

            } catch (error) {

                console.error(error);

            }

        }

        loadData();

    }, []);

    if (!dashboard || !health) {

        return (
            <Typography>
                Carregando painel...
            </Typography>
        );

    }

    return (

        <Box>

            <Typography
                variant="h4"
                fontWeight="bold"
                mb={4}
            >
                Painel
            </Typography>

            <Grid container spacing={3}>

                <Grid item xs={12} md={6} lg={3}>
                    <StatCard
                        title="Produtos"
                        value={dashboard.products}
                    />
                </Grid>

                <Grid item xs={12} md={6} lg={3}>
                    <StatCard
                        title="Pontuação"
                        value={dashboard.score}
                        color="#22C55E"
                    />
                </Grid>

                <Grid item xs={12} md={6} lg={3}>
                    <StatCard
                        title="Comissão"
                        value={`${dashboard.commission}%`}
                        color="#F59E0B"
                    />
                </Grid>

                <Grid item xs={12} md={6} lg={3}>
                    <StatCard
                        title="Produtos IA"
                        value={dashboard.ai_products}
                        color="#8B5CF6"
                    />
                </Grid>

            </Grid>

            <Typography
                variant="h5"
                mt={6}
                mb={3}
                fontWeight="bold"
            >
                Saúde do Sistema
            </Typography>

            <Grid container spacing={3}>

                <Grid item xs={12} md={4}>
                    <HealthCard
                        title="Backend"
                        status={health.backend}
                    />
                </Grid>

                <Grid item xs={12} md={4}>
                    <HealthCard
                        title="Banco de Dados"
                        status={health.database}
                    />
                </Grid>

                <Grid item xs={12} md={4}>
                    <HealthCard
                        title="Dashboard API"
                        status={health.dashboard}
                    />
                </Grid>

                <Grid item xs={12} md={4}>
                    <HealthCard
                        title="Frontend"
                        status={health.frontend}
                    />
                </Grid>

                <Grid item xs={12} md={4}>
                    <HealthCard
                        title="Scout IA"
                        status={health.scout}
                    />
                </Grid>

                <Grid item xs={12} md={4}>
                    <HealthCard
                        title="Shopee API"
                        status={health.shopee}
                    />
                </Grid>

            </Grid>

        </Box>

    );

}