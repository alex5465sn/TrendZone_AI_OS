import { Chip, Tooltip } from "@mui/material";
import StorefrontIcon from "@mui/icons-material/Storefront";

export interface MarketplaceBadgeInfo {
    label: string;
    color: string;
    textColor: string;
}

export const MARKETPLACE_BADGES: Record<string, MarketplaceBadgeInfo> = {
    shopee: { label: "Shopee", color: "#EE4D2D", textColor: "#FFFFFF" },
    mercado_livre: { label: "Mercado Livre", color: "#FFE600", textColor: "#0B1120" },
};

export function marketplaceBadgeInfo(marketplace?: string): MarketplaceBadgeInfo {
    const key = (marketplace || "shopee").toLowerCase();
    return (
        MARKETPLACE_BADGES[key] || {
            label: key.charAt(0).toUpperCase() + key.slice(1).replace("_", " "),
            color: "#334155",
            textColor: "#F8FAFC",
        }
    );
}

export function marketplaceViewLabel(marketplace?: string): string {
    const info = marketplaceBadgeInfo(marketplace);
    return `Ver na ${info.label}`;
}

export function MarketplaceBadge({ marketplace }: { marketplace?: string }) {
    const info = marketplaceBadgeInfo(marketplace);
    return (
        <Tooltip title={`Produto originado do ${info.label}`}>
            <Chip
                icon={<StorefrontIcon sx={{ color: `${info.textColor} !important` }} fontSize="small" />}
                label={info.label}
                size="small"
                sx={{
                    backgroundColor: info.color,
                    color: info.textColor,
                    fontWeight: 700,
                }}
            />
        </Tooltip>
    );
}
