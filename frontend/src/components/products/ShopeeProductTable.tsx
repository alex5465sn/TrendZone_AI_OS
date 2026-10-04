import {
    Paper,
    Table,
    TableBody,
    TableCell,
    TableContainer,
    TableHead,
    TableRow,
    Avatar,
    Box,
    Typography,
    Chip,
    IconButton,
    Tooltip,
    Checkbox,
} from "@mui/material";

import OpenInNewIcon from "@mui/icons-material/OpenInNew";
import AddIcon from "@mui/icons-material/Add";
import CheckCircleIcon from "@mui/icons-material/CheckCircle";
import CampaignIcon from "@mui/icons-material/Campaign";

import type { ShopeeProductNode } from "../../services/marketplaceService";
import { MarketplaceBadge, marketplaceViewLabel } from "../../constants/marketplaceBadge";

interface ShopeeProductTableProps {
    products: ShopeeProductNode[];
    onAdd?: (product: ShopeeProductNode) => void;
    onPromote?: (product: ShopeeProductNode) => void;
    selectedIds?: Set<number>;
    onToggleSelect?: (itemId: number) => void;
    onToggleSelectAll?: () => void;
}

export default function ShopeeProductTable({
    products,
    onAdd,
    onPromote,
    selectedIds,
    onToggleSelect,
    onToggleSelectAll,
}: ShopeeProductTableProps) {

    function formatCurrency(value: string) {

        return new Intl.NumberFormat(
            "pt-BR",
            {
                style: "currency",
                currency: "BRL",
            }
        ).format(Number(value));

    }

    function formatRate(rate: string) {

        return `${(Number(rate) * 100).toFixed(1)}%`;

    }

    function getDecision(score: number) {

        if (score >= 80) return { label: "PROMOVER", color: "success" as const };
        if (score >= 60) return { label: "TESTAR", color: "warning" as const };
        if (score >= 40) return { label: "OBSERVAR", color: "info" as const };
        return { label: "DESCARTAR", color: "error" as const };

    }

    function colorForDecision(label: string) {

        if (label === "PROMOVER") return "success" as const;
        if (label === "TESTAR") return "warning" as const;
        if (label === "OBSERVAR") return "info" as const;
        return "error" as const;

    }

    return (

        <TableContainer
            component={Paper}
            sx={{
                borderRadius: 3,
                backgroundColor: "#111827",
                border: "1px solid #1E293B",
            }}
        >

            <Table>

                <TableHead>

                    <TableRow>
                        {onToggleSelect && (
                            <TableCell padding="checkbox">
                                <Checkbox
                                    sx={{ color: "#94A3B8" }}
                                    checked={products.length > 0 && selectedIds?.size === products.length}
                                    indeterminate={!!selectedIds && selectedIds.size > 0 && selectedIds.size < products.length}
                                    onChange={() => onToggleSelectAll?.()}
                                />
                            </TableCell>
                        )}
                        <TableCell sx={{ color: "#94A3B8" }}>Origem</TableCell>
                        <TableCell sx={{ color: "#94A3B8" }}>ID</TableCell>
                        <TableCell sx={{ color: "#94A3B8" }}>Produto</TableCell>
                        <TableCell sx={{ color: "#94A3B8" }}>Loja</TableCell>
                        <TableCell sx={{ color: "#94A3B8" }}>Preço</TableCell>
                        <TableCell sx={{ color: "#94A3B8" }}>Comissão</TableCell>
                        <TableCell sx={{ color: "#94A3B8" }}>Vendas</TableCell>
                        <TableCell sx={{ color: "#94A3B8" }}>Avaliação</TableCell>
                        <TableCell sx={{ color: "#94A3B8" }}>Ações</TableCell>
                    </TableRow>

                </TableHead>

                <TableBody>

                    {products.map((product) => {

                        const score = product.score ?? Number(product.ratingStar) * 20;
                        const decisionLabel = product.decision ?? getDecision(score).label;
                        const decision = { label: decisionLabel, color: colorForDecision(decisionLabel) };
                        const canPromote = decisionLabel === "PROMOVER" || decisionLabel === "TESTAR";

                        return (

                            <TableRow
                                key={product.itemId}
                                hover
                                sx={{
                                    "&:hover": {
                                        backgroundColor: "#1E293B",
                                    },
                                }}
                            >

                                {onToggleSelect && (
                                    <TableCell padding="checkbox">
                                        <Checkbox
                                            sx={{ color: "#94A3B8" }}
                                            checked={!!selectedIds?.has(product.itemId)}
                                            onChange={() => onToggleSelect(product.itemId)}
                                        />
                                    </TableCell>
                                )}

                                <TableCell>
                                    <MarketplaceBadge marketplace={product.marketplace} />
                                </TableCell>

                                <TableCell>
                                    <Chip
                                        label={product.itemId}
                                        size="small"
                                        sx={{
                                            backgroundColor: "#1E293B",
                                            color: "#94A3B8",
                                            fontFamily: "monospace",
                                        }}
                                    />
                                </TableCell>

                                <TableCell>
                                    <Box
                                        sx={{
                                            display: "flex",
                                            alignItems: "center",
                                            gap: 2,
                                        }}
                                    >
                                        <Avatar
                                            src={product.imageUrl}
                                            alt={product.productName}
                                            variant="rounded"
                                            sx={{ width: 48, height: 48 }}
                                        />
                                        <Box>
                                            <Typography
                                                color="#F8FAFC"
                                                sx={{
                                                    maxWidth: 300,
                                                    overflow: "hidden",
                                                    textOverflow: "ellipsis",
                                                    whiteSpace: "nowrap",
                                                }}
                                            >
                                                {product.productName}
                                            </Typography>
                                            <Tooltip title={canPromote && onPromote ? "Clique para gerar o conteúdo de divulgação" : ""}>
                                                <Chip
                                                    label={decision.label}
                                                    color={decision.color}
                                                    size="small"
                                                    icon={canPromote && onPromote ? <CampaignIcon fontSize="small" /> : undefined}
                                                    onClick={canPromote && onPromote ? () => onPromote(product) : undefined}
                                                    sx={{
                                                        mt: 0.5,
                                                        fontWeight: 600,
                                                        cursor: canPromote && onPromote ? "pointer" : "default",
                                                    }}
                                                />
                                            </Tooltip>
                                        </Box>
                                    </Box>
                                </TableCell>

                                <TableCell>
                                    <Typography color="#94A3B8">
                                        {product.shopName}
                                    </Typography>
                                </TableCell>

                                <TableCell>
                                    <Typography color="#F8FAFC" fontWeight="bold">
                                        {formatCurrency(product.price)}
                                    </Typography>
                                </TableCell>

                                <TableCell>
                                    <Chip
                                        label={formatRate(product.commissionRate)}
                                        size="small"
                                        sx={{
                                            backgroundColor: "#10B98133",
                                            color: "#10B981",
                                            fontWeight: 600,
                                        }}
                                    />
                                </TableCell>

                                <TableCell>
                                    <Typography color="#F8FAFC">
                                        {product.sales}
                                    </Typography>
                                </TableCell>

                                <TableCell>
                                    <Typography color="#F8FAFC">
                                        {product.ratingStar} ★
                                    </Typography>
                                </TableCell>

                                <TableCell>
                                    <Box
                                        sx={{
                                            display: "flex",
                                            gap: 1,
                                        }}
                                    >

                                        <Tooltip title={marketplaceViewLabel(product.marketplace)}>
                                            <IconButton
                                                href={product.offerLink}
                                                target="_blank"
                                                rel="noopener noreferrer"
                                                size="small"
                                                sx={{ color: "#38BDF8" }}
                                            >
                                                <OpenInNewIcon fontSize="small" />
                                            </IconButton>
                                        </Tooltip>

                                        {product.alreadyTracked ? (
                                            <Tooltip title="Já está no banco (a IA adicionou automaticamente)">
                                                <span>
                                                    <IconButton size="small" disabled sx={{ color: "#10B981" }}>
                                                        <CheckCircleIcon fontSize="small" />
                                                    </IconButton>
                                                </span>
                                            </Tooltip>
                                        ) : (
                                            onAdd && (
                                                <Tooltip title="Adicionar ao Tracker">
                                                    <IconButton
                                                        size="small"
                                                        onClick={() => onAdd(product)}
                                                        sx={{ color: "#10B981" }}
                                                    >
                                                        <AddIcon fontSize="small" />
                                                    </IconButton>
                                                </Tooltip>
                                            )
                                        )}

                                    </Box>
                                </TableCell>

                            </TableRow>

                        );

                    })}

                </TableBody>

            </Table>

        </TableContainer>

    );

}
