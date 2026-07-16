import {

    Paper,

    Table,

    TableBody,

    TableCell,

    TableContainer,

    TableHead,

    TableRow,

} from "@mui/material";

import ProductRow from "./ProductRow";

import type {

    Product,

} from "../../services/productService";

interface ProductTableProps {

    products: Product[];

}

export default function ProductTable({

    products,

}: ProductTableProps) {

    return (

        <TableContainer
            component={Paper}
            sx={{
                mt:3,
                borderRadius:3,
            }}
        >

            <Table>

                <TableHead>

                    <TableRow>

                        <TableCell>Produto</TableCell>

                        <TableCell>Preço</TableCell>

                        <TableCell>Comissão</TableCell>

                        <TableCell>IA</TableCell>

                        <TableCell width={170}>Ações</TableCell>

                    </TableRow>

                </TableHead>

                <TableBody>

                    {

                        products.map((product)=>(

                            <ProductRow

                                key={product.id}

                                product={product}

                            />

                        ))

                    }

                </TableBody>

            </Table>

        </TableContainer>

    );

}