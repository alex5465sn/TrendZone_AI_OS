import { useEffect, useState } from 'react'
import {
  Box,
  Typography,
  Card,
  CardContent,
  Button,
  TextField,
  Checkbox,
  FormControlLabel,
  LinearProgress,
  Alert,
  Grid,
  Chip,
  CircularProgress,
} from '@mui/material'
import CheckCircleIcon from '@mui/icons-material/CheckCircle'
import PendingIcon from '@mui/icons-material/Pending'
import TrendingUpIcon from '@mui/icons-material/TrendingUp'
import api from '../../api/axios'

interface FirstSalePlanData {
  id: number
  selected_niche: string
  current_phase: string
  checklist: {
    niche_validated: boolean
    champion_products_identified: number
    whatsapp_groups_count: number
    facebook_groups_count: number
    groups_registered: boolean
  }
  metrics: {
    posts_published: number
    total_clicks: number
    total_conversions: number
    conversion_rate: number
    estimated_commission: number
    first_sale_achieved: boolean
    first_sale_date: string | null
  }
  recommendations: Array<{
    priority: string
    message: string
  }>
  notes: string
}

export default function FirstSalePlan() {
  const [plan, setPlan] = useState<FirstSalePlanData | null>(null)
  const [loading, setLoading] = useState(true)
  const [niche, setNiche] = useState('')
  const [phase, setPhase] = useState('preparation')
  const [whatsappGroups, setWhatsappGroups] = useState(0)
  const [facebookGroups, setFacebookGroups] = useState(0)
  const [championProducts, setChampionProducts] = useState(0)
  const [nicheValidated, setNicheValidated] = useState(false)
  const [groupsRegistered, setGroupsRegistered] = useState(false)

  useEffect(() => {
    fetchPlan()
  }, [])

  const fetchPlan = async () => {
    try {
      const response = await api.get('/first-sale-plan')
      setPlan(response.data.data)
      setNiche(response.data.data.selected_niche)
      setPhase(response.data.data.current_phase)
      setWhatsappGroups(response.data.data.checklist.whatsapp_groups_count)
      setFacebookGroups(response.data.data.checklist.facebook_groups_count)
      setChampionProducts(response.data.data.checklist.champion_products_identified)
      setNicheValidated(response.data.data.checklist.niche_validated)
      setGroupsRegistered(response.data.data.checklist.groups_registered)
    } catch (error) {
      console.error('Erro ao carregar plano:', error)
    } finally {
      setLoading(false)
    }
  }

  const savePlan = async () => {
    try {
      await api.put('/first-sale-plan', {
        selected_niche: niche,
        current_phase: phase,
        whatsapp_groups_count: whatsappGroups,
        facebook_groups_count: facebookGroups,
        champion_products_identified: championProducts,
        niche_validated: nicheValidated,
        groups_registered: groupsRegistered,
      })
      await fetchPlan()
    } catch (error) {
      console.error('Erro ao salvar plano:', error)
    }
  }

  const markFirstSale = async () => {
    try {
      await api.post('/first-sale-plan/mark-first-sale', {
        product_name: 'Primeira Venda',
        channel: 'whatsapp',
      })
      await fetchPlan()
    } catch (error) {
      console.error('Erro ao marcar primeira venda:', error)
    }
  }

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
        <CircularProgress />
      </Box>
    )
  }

  if (!plan) {
    return <Typography>Erro ao carregar plano</Typography>
  }

  const preparationProgress = nicheValidated && groupsRegistered && championProducts >= 5 ? 100 : 50
  const executionProgress = plan.metrics.total_clicks > 0 ? Math.min((plan.metrics.total_clicks / 50) * 100, 100) : 0
  const conversionProgress = plan.metrics.total_conversions > 0 ? 100 : 0

  return (
    <Box sx={{ p: 3, maxWidth: 1200, mx: 'auto' }}>
      <Typography variant="h4" sx={{ mb: 3, fontWeight: 'bold', color: '#F8FAFC' }}>
        🎯 Plano de Primeira Venda
      </Typography>

      {plan.metrics.first_sale_achieved && (
        <Alert severity="success" sx={{ mb: 3 }}>
          🎉 <strong>Parabéns!</strong> Primeira venda alcançada em{' '}
          {new Date(plan.metrics.first_sale_date!).toLocaleDateString('pt-BR')}
        </Alert>
      )}

      {/* Fase Atual */}
      <Card sx={{ mb: 3, backgroundColor: '#1E293B', borderColor: '#475569', border: '1px solid' }}>
        <CardContent>
          <Typography variant="h6" sx={{ mb: 2, color: '#94A3B8' }}>
            Fase Atual
          </Typography>
          <Box sx={{ display: 'flex', gap: 2, mb: 2 }}>
            <Chip
              label="Preparação"
              color={phase === 'preparation' ? 'primary' : 'default'}
              onClick={() => setPhase('preparation')}
            />
            <Chip
              label="Execução"
              color={phase === 'execution' ? 'primary' : 'default'}
              onClick={() => setPhase('execution')}
            />
            <Chip
              label="Otimização"
              color={phase === 'optimization' ? 'primary' : 'default'}
              onClick={() => setPhase('optimization')}
            />
          </Box>
        </CardContent>
      </Card>

      {/* Nicho Selecionado */}
      <Card sx={{ mb: 3, backgroundColor: '#1E293B', borderColor: '#475569', border: '1px solid' }}>
        <CardContent>
          <Typography variant="h6" sx={{ mb: 2, color: '#94A3B8' }}>
            Nicho Selecionado
          </Typography>
          <TextField
            fullWidth
            label="Qual nicho você escolheu?"
            value={niche}
            onChange={(e) => setNiche(e.target.value)}
            placeholder="Ex: Achadinhos, Moda, Beleza"
            InputLabelProps={{ sx: { color: '#94A3B8' } }}
            InputProps={{ sx: { color: '#F8FAFC' } }}
            sx={{ mb: 2 }}
          />
          <FormControlLabel
            control={<Checkbox checked={nicheValidated} onChange={(e) => setNicheValidated(e.target.checked)} />}
            label="✓ Nicho validado no Scout (score ≥70)"
            sx={{ color: '#F8FAFC' }}
          />
        </CardContent>
      </Card>

      {/* Checklist Semana 1 */}
      {phase === 'preparation' && (
        <Card sx={{ mb: 3, backgroundColor: '#1E293B', borderColor: '#475569', border: '1px solid' }}>
          <CardContent>
            <Typography variant="h6" sx={{ mb: 2, color: '#94A3B8' }}>
              📋 Checklist Semana 1
            </Typography>
            <LinearProgress variant="determinate" value={preparationProgress} sx={{ mb: 2 }} />
            <Typography variant="body2" sx={{ color: '#94A3B8', mb: 2 }}>
              Progresso: {preparationProgress}%
            </Typography>

            <Box sx={{ mb: 2 }}>
              <Typography variant="body2" sx={{ color: '#F8FAFC', mb: 1 }}>
                Produtos Campeões Identificados
              </Typography>
              <TextField
                type="number"
                value={championProducts}
                onChange={(e) => setChampionProducts(parseInt(e.target.value) || 0)}
                inputProps={{ min: 0, max: 20 }}
                sx={{ width: 100 }}
                InputProps={{ sx: { color: '#F8FAFC' } }}
              />
              <Typography variant="caption" sx={{ color: '#94A3B8', ml: 2 }}>
                Meta: 5+ produtos
              </Typography>
            </Box>

            <Box sx={{ mb: 2 }}>
              <Typography variant="body2" sx={{ color: '#F8FAFC', mb: 1 }}>
                Grupos de WhatsApp
              </Typography>
              <TextField
                type="number"
                value={whatsappGroups}
                onChange={(e) => setWhatsappGroups(parseInt(e.target.value) || 0)}
                inputProps={{ min: 0, max: 20 }}
                sx={{ width: 100 }}
                InputProps={{ sx: { color: '#F8FAFC' } }}
              />
            </Box>

            <Box sx={{ mb: 2 }}>
              <Typography variant="body2" sx={{ color: '#F8FAFC', mb: 1 }}>
                Grupos de Facebook
              </Typography>
              <TextField
                type="number"
                value={facebookGroups}
                onChange={(e) => setFacebookGroups(parseInt(e.target.value) || 0)}
                inputProps={{ min: 0, max: 20 }}
                sx={{ width: 100 }}
                InputProps={{ sx: { color: '#F8FAFC' } }}
              />
            </Box>

            <FormControlLabel
              control={<Checkbox checked={groupsRegistered} onChange={(e) => setGroupsRegistered(e.target.checked)} />}
              label="✓ Grupos cadastrados em 'Grupos de Divulgação'"
              sx={{ color: '#F8FAFC' }}
            />
          </CardContent>
        </Card>
      )}

      {/* Métricas */}
      <Grid container spacing={2} sx={{ mb: 3 }}>
        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ backgroundColor: '#1E293B', borderColor: '#475569', border: '1px solid' }}>
            <CardContent>
              <Typography variant="body2" sx={{ color: '#94A3B8', mb: 1 }}>
                Posts Publicados
              </Typography>
              <Typography variant="h5" sx={{ color: '#F8FAFC' }}>
                {plan.metrics.posts_published}
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ backgroundColor: '#1E293B', borderColor: '#475569', border: '1px solid' }}>
            <CardContent>
              <Typography variant="body2" sx={{ color: '#94A3B8', mb: 1 }}>
                Cliques
              </Typography>
              <Typography variant="h5" sx={{ color: '#F8FAFC' }}>
                {plan.metrics.total_clicks}
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ backgroundColor: '#1E293B', borderColor: '#475569', border: '1px solid' }}>
            <CardContent>
              <Typography variant="body2" sx={{ color: '#94A3B8', mb: 1 }}>
                Conversões
              </Typography>
              <Typography variant="h5" sx={{ color: '#F8FAFC' }}>
                {plan.metrics.total_conversions}
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <Card sx={{ backgroundColor: '#1E293B', borderColor: '#475569', border: '1px solid' }}>
            <CardContent>
              <Typography variant="body2" sx={{ color: '#94A3B8', mb: 1 }}>
                Taxa de Conversão
              </Typography>
              <Typography variant="h5" sx={{ color: '#F8FAFC' }}>
                {(plan.metrics.conversion_rate * 100).toFixed(2)}%
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Recomendações */}
      {plan.recommendations.length > 0 && (
        <Card sx={{ mb: 3, backgroundColor: '#1E293B', borderColor: '#475569', border: '1px solid' }}>
          <CardContent>
            <Typography variant="h6" sx={{ mb: 2, color: '#94A3B8' }}>
              💡 Recomendações
            </Typography>
            {plan.recommendations.map((rec, idx) => (
              <Alert
                key={idx}
                severity={rec.priority === 'high' ? 'warning' : rec.priority === 'medium' ? 'info' : 'success'}
                sx={{ mb: 1 }}
              >
                {rec.message}
              </Alert>
            ))}
          </CardContent>
        </Card>
      )}

      {/* Botões de Ação */}
      <Box sx={{ display: 'flex', gap: 2 }}>
        <Button variant="contained" color="primary" onClick={savePlan}>
          Salvar Plano
        </Button>
        {!plan.metrics.first_sale_achieved && (
          <Button variant="contained" color="success" onClick={markFirstSale}>
            🎉 Marcar Primeira Venda
          </Button>
        )}
      </Box>
    </Box>
  )
}
