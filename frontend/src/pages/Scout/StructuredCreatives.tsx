import React, { useState } from "react";
import {
  Box,
  Card,
  CardContent,
  CardHeader,
  Button,
  Tabs,
  Tab,
  Typography,
  Chip,
  Grid,
  Alert,
  CircularProgress,
} from "@mui/material";
import ContentCopyIcon from "@mui/icons-material/ContentCopy";
import { generateStructuredCreatives, CreativeAngle } from "../../utils/postGenerator";

interface StructuredCreativesProps {
  product: {
    productName: string;
    price: string | number;
    priceDiscountRate?: number;
    offerLink: string;
    commissionRate?: string | number;
  };
}

const ANGLE_LABELS: Record<CreativeAngle, string> = {
  [CreativeAngle.PROBLEM]: "🎯 Problema",
  [CreativeAngle.TRANSFORMATION]: "✨ Transformação",
  [CreativeAngle.THREE_REASONS]: "📋 3 Motivos",
  [CreativeAngle.DEMONSTRATION]: "🔧 Demonstração",
  [CreativeAngle.COMPARISON]: "⚖️ Comparação",
};

const ANGLE_DESCRIPTIONS: Record<CreativeAngle, string> = {
  [CreativeAngle.PROBLEM]: "Foca no problema que o produto resolve",
  [CreativeAngle.TRANSFORMATION]: "Mostra antes/depois, transformação visual",
  [CreativeAngle.THREE_REASONS]: "Apresenta 3 razões para comprar",
  [CreativeAngle.DEMONSTRATION]: "Como funciona, demonstração prática",
  [CreativeAngle.COMPARISON]: "Comparação com alternativas/concorrentes",
};

export const StructuredCreatives: React.FC<StructuredCreativesProps> = ({
  product,
}) => {
  const [selectedAngle, setSelectedAngle] = useState<CreativeAngle>(
    CreativeAngle.PROBLEM
  );
  const [creatives, setCreatives] = useState<Record<CreativeAngle, string> | null>(null);
  const [loading, setLoading] = useState(false);
  const [copied, setCopied] = useState(false);

  const handleGenerateCreatives = () => {
    setLoading(true);
    try {
      const generated = generateStructuredCreatives(product);
      setCreatives(generated);
    } catch (error) {
      console.error("Erro ao gerar criativos estruturados:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleCopyCreative = () => {
    if (creatives && creatives[selectedAngle]) {
      navigator.clipboard.writeText(creatives[selectedAngle]);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  const angles = Object.values(CreativeAngle);

  return (
    <Box sx={{ mt: 3 }}>
      <Card>
        <CardHeader
          title="🎨 Criativos Estruturados (Fase 2)"
          subheader="5 ângulos diferentes para testar qual converte melhor"
        />
        <CardContent>
          {!creatives ? (
            <Box sx={{ textAlign: "center", py: 3 }}>
              <Typography variant="body2" color="textSecondary" sx={{ mb: 2 }}>
                Gere 5 criativos com ângulos diferentes para o mesmo produto.
                Cada um é otimizado para um tipo diferente de persuasão.
              </Typography>
              <Button
                variant="contained"
                color="primary"
                onClick={handleGenerateCreatives}
                disabled={loading}
              >
                {loading ? (
                  <>
                    <CircularProgress size={20} sx={{ mr: 1 }} />
                    Gerando...
                  </>
                ) : (
                  "Gerar 5 Criativos"
                )}
              </Button>
            </Box>
          ) : (
            <>
              <Alert severity="info" sx={{ mb: 2 }}>
                ✅ 5 criativos gerados! Teste cada ângulo em grupos/canais
                diferentes para descobrir qual converte melhor.
              </Alert>

              <Tabs
                value={selectedAngle}
                onChange={(_, value) => setSelectedAngle(value)}
                variant="scrollable"
                scrollButtons="auto"
                sx={{ mb: 2, borderBottom: 1, borderColor: "divider" }}
              >
                {angles.map((angle) => (
                  <Tab
                    key={angle}
                    label={ANGLE_LABELS[angle]}
                    value={angle}
                  />
                ))}
              </Tabs>

              <Box sx={{ mb: 2 }}>
                <Typography variant="subtitle2" color="textSecondary">
                  {ANGLE_DESCRIPTIONS[selectedAngle]}
                </Typography>
              </Box>

              <Card variant="outlined" sx={{ mb: 2, bgcolor: "#f5f5f5" }}>
                <CardContent>
                  <Typography
                    variant="body2"
                    component="pre"
                    sx={{
                      whiteSpace: "pre-wrap",
                      wordBreak: "break-word",
                      fontFamily: "monospace",
                      fontSize: "0.85rem",
                      lineHeight: 1.6,
                    }}
                  >
                    {creatives[selectedAngle]}
                  </Typography>
                </CardContent>
              </Card>

              <Box sx={{ display: "flex", gap: 1, flexWrap: "wrap" }}>
                <Button
                  variant="contained"
                  startIcon={<ContentCopyIcon />}
                  onClick={handleCopyCreative}
                  color={copied ? "success" : "primary"}
                >
                  {copied ? "✓ Copiado!" : "Copiar Criativo"}
                </Button>
                <Button
                  variant="outlined"
                  onClick={handleGenerateCreatives}
                >
                  Gerar Novamente
                </Button>
              </Box>

              <Box sx={{ mt: 3 }}>
                <Typography variant="subtitle2" sx={{ mb: 1, fontWeight: 600 }}>
                  📊 Dica de Teste:
                </Typography>
                <Typography variant="body2" color="textSecondary">
                  Publique cada criativo em um grupo/canal diferente. Meça
                  cliques e vendas. O ângulo que converter melhor é seu
                  vencedor — duplique esse criativo com variações.
                </Typography>
              </Box>
            </>
          )}
        </CardContent>
      </Card>
    </Box>
  );
};
