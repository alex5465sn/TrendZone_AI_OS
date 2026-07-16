import {
    Card,
    CardContent,
    Typography,
    Box,
} from "@mui/material";

interface StatCardProps {
    title: string;
    value: string | number;
    color?: string;
}

export default function StatCard({
    title,
    value,
    color = "#3B82F6",
}: StatCardProps) {
    return (
        <Card
            sx={{
                borderRadius: 3,
                background: "#1E293B",
                color: "white",
                height: "100%",
                boxShadow: "0 8px 20px rgba(0,0,0,.25)",
            }}
        >
            <CardContent>
                <Typography
                    variant="body2"
                    sx={{
                        color: "#94A3B8",
                        mb: 1,
                    }}
                >
                    {title}
                </Typography>

                <Box
                    sx={{
                        display: "flex",
                        alignItems: "center",
                    }}
                >
                    <Typography
                        variant="h4"
                        fontWeight="bold"
                        sx={{
                            color,
                        }}
                    >
                        {value}
                    </Typography>
                </Box>
            </CardContent>
        </Card>
    );
}