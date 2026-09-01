import {
    Card,
    CardContent,
    Typography,
    Box,
} from "@mui/material";

interface HealthCardProps {
    title: string;
    status: string;
}

export default function HealthCard({
    title,
    status,
}: HealthCardProps) {

    function getColor() {

        const s = status.toLowerCase();

        if (s.includes("online") || s.includes("ready") || s.includes("ok")) {
            return "#22C55E";
        }

        if (s.includes("development") || s.includes("warning") || s.includes("starting")) {
            return "#F59E0B";
        }

        if (s.includes("disconnected") || s.includes("offline") || s.includes("error")) {
            return "#EF4444";
        }

        return "#94A3B8";

    }

    return (

        <Card
            sx={{
                background: "#111827",
                borderRadius: 3,
                color: "white",
                border: "1px solid #1E293B",
                height: "100%",
            }}
        >

            <CardContent>

                <Typography
                    variant="subtitle2"
                    color="#94A3B8"
                >
                    {title}
                </Typography>

                <Box
                    display="flex"
                    alignItems="center"
                    mt={2}
                >

                    <Box
                        sx={{
                            width: 12,
                            height: 12,
                            borderRadius: "50%",
                            bgcolor: getColor(),
                            mr: 1.5,
                            boxShadow: `0 0 8px ${getColor()}`,
                        }}
                    />

                    <Typography
                        fontWeight="bold"
                        textTransform="capitalize"
                    >
                        {status}
                    </Typography>

                </Box>

            </CardContent>

        </Card>

    );

}
