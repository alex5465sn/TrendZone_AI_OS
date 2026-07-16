import {
    TableRow,
    TableCell,
    Chip,
    Stack,
    IconButton,
    Tooltip,
} from "@mui/material";

import VisibilityIcon from "@mui/icons-material/Visibility";
import EditIcon from "@mui/icons-material/Edit";
import DeleteIcon from "@mui/icons-material/Delete";

interface ProductRowProps {

    product: {

        id: number;

        name: string;

        price: number;

        commission: number;

        score: number;

    };

}

export default function ProductRow({

    product,

}: ProductRowProps) {

    let decision = "DESCARTAR";
    let color: "success" | "warning" | "info" | "error" = "error";

    if (product.score >= 80) {

        decision = "PROMOVER";
        color = "success";

    }

    else if (product.score >= 60) {

        decision = "TESTAR";
        color = "warning";

    }

    else if (product.score >= 40) {

        decision = "OBSERVAR";
        color = "info";

    }

    return (

        <TableRow hover>

            <TableCell>

                {product.name}

            </TableCell>

            <TableCell>

                {
                    new Intl.NumberFormat(

                        "pt-BR",

                        {

                            style: "currency",

                            currency: "BRL",

                        }

                    ).format(product.price)
                }

            </TableCell>

            <TableCell>

                {product.commission.toFixed(1)}%

            </TableCell>

            <TableCell>

                <Chip

                    label={`${product.score} • ${decision}`}

                    color={color}

                    size="small"

                />

            </TableCell>

            <TableCell>

                <Stack
                    direction="row"
                    spacing={1}
                >

                    <Tooltip title="Visualizar">

                        <IconButton size="small">

                            <VisibilityIcon fontSize="small"/>

                        </IconButton>

                    </Tooltip>

                    <Tooltip title="Editar">

                        <IconButton size="small">

                            <EditIcon fontSize="small"/>

                        </IconButton>

                    </Tooltip>

                    <Tooltip title="Excluir">

                        <IconButton
                            size="small"
                            color="error"
                        >

                            <DeleteIcon fontSize="small"/>

                        </IconButton>

                    </Tooltip>

                </Stack>

            </TableCell>

        </TableRow>

    );

}