import {
    TextField,
} from "@mui/material";

interface ProductSearchProps {
    value: string;
    onChange: (value: string) => void;
}

export default function ProductSearch({
    value,
    onChange,
}: ProductSearchProps) {

    return (

        <TextField
            fullWidth
            label="Pesquisar Produto"
            variant="outlined"
            value={value}
            onChange={(event) => onChange(event.target.value)}
            sx={{
                mb: 3,
                backgroundColor: "#111827",
                borderRadius: 2,
            }}
        />

    );

}