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

        switch (status) {

            case "online":
                return "#22C55E";

            case "development":
                return "#F59E0B";

            case "disconnected":
                return "#94A3B8";

            default:
                return "#EF4444";

        }

    }

    return (

        <Card
            sx={{
                background: "#111827",
                borderRadius: 3,
                color: "white",
                border: "1px solid #1E293B",
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
                        }}
                    />

                    <Typography
                        fontWeight="bold"
                    >
                        {status}
                    </Typography>

                </Box>

            </CardContent>

        </Card>

    );

}