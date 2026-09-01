import {
    Card,
    CardContent,
    Typography,
    Box,
} from "@mui/material";
import type { OverridableComponent } from "@mui/material/OverridableComponent";
import type { SvgIconTypeMap } from "@mui/material/SvgIcon";

interface StatCardProps {
    title: string;
    value: string | number;
    subtitle?: string;
    icon: OverridableComponent<SvgIconTypeMap>;
    color: string;
}

export default function StatCard({
    title,
    value,
    subtitle,
    icon: Icon,
    color,
}: StatCardProps) {
    return (
        <Card
            sx={{
                background: `linear-gradient(135deg, ${color}22 0%, ${color}11 100%)`,
                border: `1px solid ${color}33`,
                borderRadius: 3,
                color: "#FFF",
                height: "100%",
                position: "relative",
                overflow: "hidden",
            }}
        >
            <CardContent>
                <Box
                    sx={{
                        display: "flex",
                        alignItems: "center",
                        justifyContent: "space-between",
                        mb: 2,
                    }}
                >
                    <Typography
                        variant="body2"
                        sx={{
                            color: "#94A3B8",
                            fontWeight: 500,
                        }}
                    >
                        {title}
                    </Typography>

                    <Box
                        sx={{
                            p: 1,
                            borderRadius: 2,
                            backgroundColor: `${color}33`,
                            color: color,
                            display: "flex",
                            alignItems: "center",
                            justifyContent: "center",
                        }}
                    >
                        <Icon fontSize="small" />
                    </Box>
                </Box>

                <Typography
                    variant="h4"
                    fontWeight="bold"
                    sx={{
                        color: "#F8FAFC",
                    }}
                >
                    {value}
                </Typography>

                {subtitle && (
                    <Typography
                        variant="body2"
                        sx={{
                            color: "#94A3B8",
                            mt: 1,
                        }}
                    >
                        {subtitle}
                    </Typography>
                )}
            </CardContent>
        </Card>
    );
}
