import { useState } from "react";

import {
    Box,
    Button,
    Paper,
    Stack,
    TextField,
    Typography,
} from "@mui/material";

import { createProduct } from "../../services/productService";

interface Props {
    onCreated: () => void;
}

export default function ProductForm({ onCreated }: Props) {

    const [itemId, setItemId] = useState("");

    const [shopId, setShopId] = useState("");

    const [name, setName] = useState("");

    const [price, setPrice] = useState("");

    const [commission, setCommission] = useState("");

    const [image, setImage] = useState("");

    const [offerLink, setOfferLink] = useState("");

    async function handleSubmit() {

        try {

            await createProduct({

                item_id: Number(itemId),

                shop_id: Number(shopId),

                name,

                price: Number(price),

                commission: Number(commission),

                image,

                offer_link: offerLink,

            });

            setItemId("");

            setShopId("");

            setName("");

            setPrice("");

            setCommission("");

            setImage("");

            setOfferLink("");

            onCreated();

        }

        catch (error) {

            console.error(error);

            alert("Erro ao salvar produto.");

        }

    }

    return (

        <Paper
            elevation={3}
            sx={{
                p: 3,
                mb: 4,
                borderRadius: 3,
            }}
        >

            <Typography
                variant="h6"
                fontWeight="bold"
                mb={3}
            >
                Novo Produto
            </Typography>

            <Stack spacing={2}>

                <TextField
                    label="Item ID Shopee"
                    value={itemId}
                    onChange={(e) => setItemId(e.target.value)}
                />

                <TextField
                    label="Shop ID"
                    value={shopId}
                    onChange={(e) => setShopId(e.target.value)}
                />

                <TextField
                    label="Nome do Produto"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                />

                <TextField
                    label="Preço"
                    type="number"
                    value={price}
                    onChange={(e) => setPrice(e.target.value)}
                />

                <TextField
                    label="Comissão (%)"
                    type="number"
                    value={commission}
                    onChange={(e) => setCommission(e.target.value)}
                />

                <TextField
                    label="Imagem"
                    value={image}
                    onChange={(e) => setImage(e.target.value)}
                />

                <TextField
                    label="Link de Afiliado"
                    value={offerLink}
                    onChange={(e) => setOfferLink(e.target.value)}
                />

                <Box>

                    <Button
                        variant="contained"
                        size="large"
                        onClick={handleSubmit}
                    >
                        Salvar Produto
                    </Button>

                </Box>

            </Stack>

        </Paper>

    );

}