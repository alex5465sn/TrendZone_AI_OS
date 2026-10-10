import React, { useEffect, useState } from "react";
import {
  Box,
  Card,
  CardContent,
  CardHeader,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Chip,
  CircularProgress,
  Alert,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Typography,
} from "@mui/material";
import TrendingUpIcon from "@mui/icons-material/TrendingUp";
import TrendingDownIcon from "@mui/icons-material/TrendingDown";
import FileCopyIcon from "@mui/icons-material/FileCopy";
import { getData } from "../../services/apiResponse";

interface Winner {
  product_item_id: number;
  product_name: string;
  product_image?: string;
  total_clicks: number;
  total_sales: number;
  sales_24h: number;
  conversion_rate: number;
  total_commission: number;
  momentum: number;
  decision: string;
  reason: string;
}

const DECISION_COLORS: Record<string, "success" | "warning" | "error" | "info"> = {
  DUPLICAR: "success",
  OTIMIZAR: "warning",
  PAUSAR: "error",
  OBSERVAR: "info",
};

const DECISION_LABELS: Record<string, string> = {
  DUPLICAR: "🚀 Duplicar",
  OTIMIZAR: "⚙️ Otimizar",
  PAUSAR: "⏸️ Pausar",
  OBSERVAR: "👁️ Observar",
};

export const Winners: React.FC = () => {
  const [winners, setWinners] = useState<Winner[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedWinner, setSelectedWinner] = useState<Winner | null>(null);
  const [detailsOpen, setDetailsOpen] = useState(false);

  useEffect(() => {
    fetchWinners();
  }, []);

  const fetchWinners = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await getData<{ winners: Winner[] }>("/discovery/winners?limit=10&days=7");
      if (data.winners) {
        setWinners(data.winners);
      } else {
        setError("Nenhum vencedor encontrado ainda");
      }
    } catch (err) {
      console.error("Erro ao buscar vencedores:", err);
      setError("Erro ao carregar vencedores");
    } finally {
      setLoading(false);
    }
  };

  const handleViewDetails = (winner: Winner) => {
    setSelectedWinner(winner);
    setDetailsOpen(true);
  };

  const handleCloseDetails = () => {
    setDetailsOpen(false);
    setSelectedWinner(null);
  };

  const handleDuplicateCreatives = (winner: Winner) => {
    // Aqui você pode integrar com o gerador de criativos estruturados
    console.log("Duplicar criativos para:", winner.product_name);
    alert(`Duplicar criativos para: ${winner.product_name}\n\nEsta ação abrirá o gerador de criativos estruturados.`);
  };

  if (loading) {
    return (
      <Box sx={{ display: "flex", justifyContent: "center", py: 4 }}>
        <CircularProgress />
      </Box>
    );
  }

  if (error && winners.length === 0) {
    return (
      <Alert severity="info" sx={{ mt: 2 }}>
        {error}
      </Alert>
    );
  }

  return (
    <Box sx={{ mt: 3 }}>
      <Card>
        <CardHeader
          title="🏆 Produtos Vencedores (Fase 3)"
          subheader="Baseado em cliques reais + vendas confirmadas"
        />
        <CardContent>
          {winners.length === 0 ? (
            <Alert severity="info">
              Nenhum produto com vendas confirmadas nos últimos 7 dias.
              Comece a publicar e acompanhe aqui!
            </Alert>
          ) : (
            <>
              <Alert severity="success" sx={{ mb: 2 }}>
                ✅ {winners.length} produto(s) com vendas confirmadas.
                Siga as recomendações para escalar os vencedores!
              </Alert>

              <TableContainer>
                <Table size="small">
                  <TableHead>
                    <TableRow sx={{ bgcolor: "#f5f5f5" }}>
                      <TableCell>Produto</TableCell>
                      <TableCell align="right">Cliques</TableCell>
                      <TableCell align="right">Vendas</TableCell>
                      <TableCell align="right">Conversão</TableCell>
                      <TableCell align="right">Comissão</TableCell>
                      <TableCell align="center">Momentum</TableCell>
                      <TableCell align="center">Ação</TableCell>
                      <TableCell align="center">Detalhes</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {winners.map((winner) => (
                      <TableRow key={winner.product_item_id} hover>
                        <TableCell sx={{ maxWidth: 200 }}>
                          <Typography variant="body2" noWrap>
                            {winner.product_name}
                          </Typography>
                        </TableCell>
                        <TableCell align="right">
                          <Typography variant="body2" sx={{ fontWeight: 600 }}>
                            {winner.total_clicks}
                          </Typography>
                        </TableCell>
                        <TableCell align="right">
                          <Typography variant="body2" sx={{ fontWeight: 600, color: "green" }}>
                            {winner.total_sales}
                          </Typography>
                        </TableCell>
                        <TableCell align="right">
                          <Typography variant="body2">
                            {winner.conversion_rate.toFixed(1)}%
                          </Typography>
                        </TableCell>
                        <TableCell align="right">
                          <Typography variant="body2" sx={{ fontWeight: 600 }}>
                            R$ {winner.total_commission.toFixed(2)}
                          </Typography>
                        </TableCell>
                        <TableCell align="center">
                          {winner.momentum > 0 ? (
                            <Box sx={{ display: "flex", alignItems: "center", justifyContent: "center", gap: 0.5 }}>
                              <TrendingUpIcon sx={{ color: "green", fontSize: 18 }} />
                              <Typography variant="caption" sx={{ color: "green", fontWeight: 600 }}>
                                +{winner.momentum.toFixed(0)}%
                              </Typography>
                            </Box>
                          ) : winner.momentum < 0 ? (
                            <Box sx={{ display: "flex", alignItems: "center", justifyContent: "center", gap: 0.5 }}>
                              <TrendingDownIcon sx={{ color: "red", fontSize: 18 }} />
                              <Typography variant="caption" sx={{ color: "red", fontWeight: 600 }}>
                                {winner.momentum.toFixed(0)}%
                              </Typography>
                            </Box>
                          ) : (
                            <Typography variant="caption">—</Typography>
                          )}
                        </TableCell>
                        <TableCell align="center">
                          <Chip
                            label={DECISION_LABELS[winner.decision]}
                            color={DECISION_COLORS[winner.decision]}
                            size="small"
                            variant="outlined"
                          />
                        </TableCell>
                        <TableCell align="center">
                          <Button
                            size="small"
                            onClick={() => handleViewDetails(winner)}
                          >
                            Ver
                          </Button>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>

              <Box sx={{ mt: 2 }}>
                <Button
                  variant="outlined"
                  onClick={fetchWinners}
                  size="small"
                >
                  Atualizar
                </Button>
              </Box>
            </>
          )}
        </CardContent>
      </Card>

      {/* Dialog de Detalhes */}
      <Dialog open={detailsOpen} onClose={handleCloseDetails} maxWidth="sm" fullWidth>
        <DialogTitle>
          🏆 Detalhes do Vencedor
        </DialogTitle>
        <DialogContent>
          {selectedWinner && (
            <Box sx={{ mt: 2 }}>
              <Typography variant="subtitle2" sx={{ fontWeight: 600, mb: 1 }}>
                {selectedWinner.product_name}
              </Typography>

              <Box sx={{ mb: 2, p: 1.5, bgcolor: "#f5f5f5", borderRadius: 1 }}>
                <Typography variant="caption" display="block">
                  <strong>Cliques:</strong> {selectedWinner.total_clicks}
                </Typography>
                <Typography variant="caption" display="block">
                  <strong>Vendas:</strong> {selectedWinner.total_sales}
                </Typography>
                <Typography variant="caption" display="block">
                  <strong>Conversão:</strong> {selectedWinner.conversion_rate.toFixed(2)}%
                </Typography>
                <Typography variant="caption" display="block">
                  <strong>Comissão Total:</strong> R$ {selectedWinner.total_commission.toFixed(2)}
                </Typography>
                <Typography variant="caption" display="block">
                  <strong>Vendas (24h):</strong> {selectedWinner.sales_24h}
                </Typography>
                <Typography variant="caption" display="block">
                  <strong>Momentum:</strong> {selectedWinner.momentum > 0 ? "+" : ""}{selectedWinner.momentum.toFixed(1)}%
                </Typography>
              </Box>

              <Box sx={{ mb: 2, p: 1.5, bgcolor: "#e8f5e9", borderRadius: 1 }}>
                <Typography variant="subtitle2" sx={{ fontWeight: 600, mb: 0.5 }}>
                  Recomendação: {DECISION_LABELS[selectedWinner.decision]}
                </Typography>
                <Typography variant="body2">
                  {selectedWinner.reason}
                </Typography>
              </Box>

              {selectedWinner.decision === "DUPLICAR" && (
                <Alert severity="success" sx={{ mb: 2 }}>
                  Este produto é um vencedor claro! Duplique os criativos que
                  funcionaram e teste variações para escalar ainda mais.
                </Alert>
              )}

              {selectedWinner.decision === "OTIMIZAR" && (
                <Alert severity="warning" sx={{ mb: 2 }}>
                  Bom desempenho, mas pode melhorar. Teste novos ângulos de
                  criativo ou ajuste a oferta.
                </Alert>
              )}

              {selectedWinner.decision === "PAUSAR" && (
                <Alert severity="error" sx={{ mb: 2 }}>
                  Sem vendas ou taxa de conversão muito baixa. Considere pausar
                  ou testar um criativo completamente diferente.
                </Alert>
              )}
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          {selectedWinner?.decision === "DUPLICAR" && (
            <Button
              variant="contained"
              startIcon={<FileCopyIcon />}
              onClick={() => {
                handleDuplicateCreatives(selectedWinner);
                handleCloseDetails();
              }}
            >
              Duplicar Criativos
            </Button>
          )}
          <Button onClick={handleCloseDetails}>Fechar</Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};
