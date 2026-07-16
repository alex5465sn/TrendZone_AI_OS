import {
    Box,
    Chip,
} from "@mui/material";

export default function ProductFilters() {

    return (

        <Box
            display="flex"
            gap={1}
            mb={3}
            flexWrap="wrap"
        >

            <Chip label="Todos" color="primary" />

            <Chip label="Alta Comissão" />

            <Chip label="Maior Score" />

            <Chip label="Em Alta" />

            <Chip label="IA Recomenda" />

        </Box>

    );

}