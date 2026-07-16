import { useEffect, useState } from "react";

import {
    Box,
    Typography,
    CircularProgress,
    Alert,
} from "@mui/material";

import ProductSearch from "../../components/products/ProductSearch";
import ProductFilters from "../../components/products/ProductFilters";
import ProductForm from "../../components/products/ProductForm";
import ProductTable from "../../components/products/ProductTable";

import {
    getProducts,
    type Product,
} from "../../services/productService";

export default function Products() {

    const [products, setProducts] = useState<Product[]>([]);

    const [loading, setLoading] = useState(true);

    const [error, setError] = useState("");

    async function loadProducts() {

        try {

            setLoading(true);

            const data = await getProducts();

            setProducts(data);

            setError("");

        }

        catch (err) {

            console.error(err);

            setError("Erro ao carregar produtos.");

        }

        finally {

            setLoading(false);

        }

    }

    useEffect(() => {

        loadProducts();

    }, []);

    if (loading) {

        return <CircularProgress />;

    }

    if (error) {

        return <Alert severity="error">{error}</Alert>;

    }

    return (

        <Box>

            <Typography
                variant="h4"
                fontWeight="bold"
                mb={4}
            >
                Produtos
            </Typography>

            <ProductSearch
                value=""
                onChange={() => {}}
            />

            <ProductFilters />

            <ProductForm
                onCreated={loadProducts}
            />

            <ProductTable
                products={products}
            />

        </Box>

    );

}