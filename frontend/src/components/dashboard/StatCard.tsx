import {
    Card,
    CardContent,
    Typography,
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
                backgroundColor: "#1E293B",
                borderRadius: 3,
                color: "#FFF",
                height: "100%",
            }}
        >
            <CardContent>

                <Typography
                    variant="body2"
                    sx={{
                        color: "#94A3B8",
                    }}
                >
                    {title}
                </Typography>

                <Typography
                    variant="h4"
                    fontWeight="bold"
                    sx={{
                        color,
                        mt: 2,
                    }}
                >
                    {value}
                </Typography>

            </CardContent>
        </Card>
    );
}