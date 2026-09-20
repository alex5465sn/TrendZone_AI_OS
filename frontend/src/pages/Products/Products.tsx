import { useEffect, useState, useCallback } from "react";

import {
    Box,
    Typography,
    CircularProgress,
    Alert,
    Button,
    TextField,
    Grid,
    Chip,
} from "@mui/material";

import SearchIcon from "@mui/icons-material/Search";
import TrendingUpIcon from "@mui/icons-material/TrendingUp";
import AttachMoneyIcon from "@mui/icons-material/AttachMoney";
import StarIcon from "@mui/icons-material/Star";

import ShopeeProductTable from "../../components/products/ShopeeProductTable";
import {
    searchShopeeProducts,
    type ShopeeProductNode,
} from "../../services/marketplaceService";
import { createProduct } from "../../services/productService";

const categories = [
    "Eletrônicos",
    "Casa",
    "Moda",
    "Beleza",
    "Esportes",
    "Brinquedos",
    "Automotivo",
];

export default function Products() {

    const [products, setProducts] = useState<ShopeeProductNode[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");
    const [keyword, setKeyword] = useState("tendencia");
    const [activeCategory, setActiveCategory] = useState<string | null>(null);

    const loadProducts = useCallback(async (search: string) => {

        try {

            setLoading(true);
            setError("");

            const data = await searchShopeeProducts({
                keyword: search,
                page: 1,
                limit: 20,
                sortType: 1,
            });

            setProducts(data.nodes || []);

        } catch (err) {

            console.error(err);
            setError("Erro ao buscar produtos na Shopee.");

        } finally {

            setLoading(false);

        }

    }, []);

    useEffect(() => {

        loadProducts(keyword);

    }, [keyword, loadProducts]);

    function handleSearch() {

        loadProducts(keyword);

    }

    function handleCategory(category: string) {

        setActiveCategory(category);
        setKeyword(category);

    }

    async function handleAdd(product: ShopeeProductNode) {

        try {

            await createProduct({
                item_id: product.itemId,
                shop_id: product.shopId,
                name: product.productName,
                price: Number(product.price),
                commission: Number(product.commissionRate) * 100,
                image: product.imageUrl,
                offer_link: product.offerLink,
                rating: Number(product.ratingStar) || 0,
                sales: Number(product.sales) || 0,
            });

            alert(`✓ Produto "${product.productName}" adicionado ao tracker!`);

        } catch (err: any) {

            if (err?.response?.status === 409) {
                alert(`Produto "${product.productName}" já está rastreado.`);
            } else {
                alert("Erro ao adicionar produto ao tracker.");
            }

        }

    }

    if (loading) {

        return (
            <Box display="flex" justifyContent="center" alignItems="center" minHeight="60vh">
                <CircularProgress />
            </Box>
        );

    }

    return (

        <Box>

            <Typography
                variant="h4"
                fontWeight="bold"
                color="#F8FAFC"
                mb={1}
            >
                Produtos Shopee
            </Typography>

            <Typography
                variant="body1"
                color="#94A3B8"
                mb={4}
            >
                Busque produtos em tempo real e identifique oportunidades de afiliados.
            </Typography>

            <Box
                sx={{
                    display: "flex",
                    gap: 2,
                    mb: 3,
                    flexWrap: "wrap",
                }}
            >

                <TextField
                    value={keyword}
                    onChange={(e) => setKeyword(e.target.value)}
                    onKeyDown={(e) => e.key === "Enter" && handleSearch()}
                    placeholder="Ex: fone de ouvido, smartwatch, bolsas..."
                    sx={{
                        flex: 1,
                        minWidth: 300,
                        backgroundColor: "#111827",
                        borderRadius: 2,
                        input: { color: "#F8FAFC" },
                    }}
                />

                <Button
                    variant="contained"
                    startIcon={<SearchIcon />}
                    onClick={handleSearch}
                    sx={{
                        backgroundColor: "#2563EB",
                        textTransform: "none",
                        borderRadius: 2,
                        px: 4,
                    }}
                >
                    Buscar
                </Button>

            </Box>

            <Box
                sx={{
                    display: "flex",
                    gap: 1,
                    mb: 4,
                    flexWrap: "wrap",
                }}
            >

                {categories.map((category) => (

                    <Chip
                        key={category}
                        label={category}
                        onClick={() => handleCategory(category)}
                        sx={{
                            backgroundColor: activeCategory === category ? "#2563EB" : "#1E293B",
                            color: "#F8FAFC",
                            fontWeight: 500,
                            cursor: "pointer",
                            "&:hover": {
                                backgroundColor: "#2563EB",
                            },
                        }}
                    />

                ))}

            </Box>

            <Grid container spacing={3} mb={4}>

                <Grid item xs={12} md={4}>
                    <Box
                        sx={{
                            p: 3,
                            borderRadius: 3,
                            backgroundColor: "#111827",
                            border: "1px solid #1E293B",
                        }}
                    >
                        <Typography color="#94A3B8" mb={1}>
                            <TrendingUpIcon sx={{ verticalAlign: "middle", mr: 1 }} />
                            Produtos Encontrados
                        </Typography>
                        <Typography variant="h4" fontWeight="bold" color="#F8FAFC">
                            {products.length}
                        </Typography>
                    </Box>
                </Grid>

                <Grid item xs={12} md={4}>
                    <Box
                        sx={{
                            p: 3,
                            borderRadius: 3,
                            backgroundColor: "#111827",
                            border: "1px solid #1E293B",
                        }}
                    >
                        <Typography color="#94A3B8" mb={1}>
                            <AttachMoneyIcon sx={{ verticalAlign: "middle", mr: 1 }} />
                            Maior Comissão
                        </Typography>
                        <Typography variant="h4" fontWeight="bold" color="#F8FAFC">
                            {products.length > 0
                                ? `${Math.max(...products.map((p) => Number(p.commissionRate) * 100)).toFixed(1)}%`
                                : "-"}
                        </Typography>
                    </Box>
                </Grid>

                <Grid item xs={12} md={4}>
                    <Box
                        sx={{
                            p: 3,
                            borderRadius: 3,
                            backgroundColor: "#111827",
                            border: "1px solid #1E293B",
                        }}
                    >
                        <Typography color="#94A3B8" mb={1}>
                            <StarIcon sx={{ verticalAlign: "middle", mr: 1 }} />
                            Melhor Avaliação
                        </Typography>
                        <Typography variant="h4" fontWeight="bold" color="#F8FAFC">
                            {products.length > 0
                                ? Math.max(...products.map((p) => Number(p.ratingStar))).toFixed(1)
                                : "-"}
                        </Typography>
                    </Box>
                </Grid>

            </Grid>

            {error && (
                <Alert severity="error" sx={{ mb: 3 }}>
                    {error}
                </Alert>
            )}

            <ShopeeProductTable
                products={products}
                onAdd={handleAdd}
            />

        </Box>

    );

}
