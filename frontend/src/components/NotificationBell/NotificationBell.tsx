import { useEffect, useState } from 'react'
import {
  IconButton,
  Badge,
  Menu,
  MenuItem,
  Typography,
  Box,
  Divider,
  Button,
} from '@mui/material'
import NotificationsIcon from '@mui/icons-material/Notifications'
import api from '../../api/axios'

interface Notification {
  id: number
  type: string
  title: string
  message: string
  sent: boolean
  read: boolean
  created_at: string
}

export default function NotificationBell() {
  const [notifications, setNotifications] = useState<Notification[]>([])
  const [unreadCount, setUnreadCount] = useState(0)
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null)
  const open = Boolean(anchorEl)

  useEffect(() => {
    fetchNotifications()
    const interval = setInterval(fetchNotifications, 30000) // Atualiza a cada 30s
    return () => clearInterval(interval)
  }, [])

  const fetchNotifications = async () => {
    try {
      const response = await api.get('/notifications')
      setNotifications(response.data.data)

      const unread = response.data.data.filter((n: Notification) => !n.read).length
      setUnreadCount(unread)
    } catch (error) {
      console.error('Erro ao carregar notificações:', error)
    }
  }

  const handleClick = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget)
  }

  const handleClose = () => {
    setAnchorEl(null)
  }

  const handleMarkAsRead = async (notificationId: number) => {
    try {
      await api.put(`/notifications/${notificationId}/read`)
      fetchNotifications()
    } catch (error) {
      console.error('Erro ao marcar como lida:', error)
    }
  }

  return (
    <>
      <IconButton
        onClick={handleClick}
        sx={{ color: '#F8FAFC' }}
      >
        <Badge badgeContent={unreadCount} color="error">
          <NotificationsIcon />
        </Badge>
      </IconButton>

      <Menu
        anchorEl={anchorEl}
        open={open}
        onClose={handleClose}
        PaperProps={{
          sx: {
            backgroundColor: '#1E293B',
            color: '#F8FAFC',
            maxWidth: 400,
            maxHeight: 500,
          },
        }}
      >
        <Box sx={{ p: 2 }}>
          <Typography variant="h6" sx={{ fontWeight: 'bold' }}>
            Notificações
          </Typography>
        </Box>
        <Divider sx={{ borderColor: '#475569' }} />

        {notifications.length === 0 ? (
          <MenuItem disabled>
            <Typography variant="body2" sx={{ color: '#94A3B8' }}>
              Nenhuma notificação
            </Typography>
          </MenuItem>
        ) : (
          notifications.slice(0, 10).map((notification) => (
            <Box key={notification.id}>
              <MenuItem
                onClick={() => handleMarkAsRead(notification.id)}
                sx={{
                  backgroundColor: notification.read ? 'transparent' : '#0F172A',
                  '&:hover': { backgroundColor: '#334155' },
                  flexDirection: 'column',
                  alignItems: 'flex-start',
                  py: 1.5,
                }}
              >
                <Typography variant="body2" sx={{ fontWeight: 'bold', mb: 0.5 }}>
                  {notification.title}
                </Typography>
                <Typography variant="caption" sx={{ color: '#94A3B8' }}>
                  {notification.message}
                </Typography>
                <Typography variant="caption" sx={{ color: '#64748B', mt: 0.5 }}>
                  {new Date(notification.created_at).toLocaleString('pt-BR')}
                </Typography>
              </MenuItem>
              <Divider sx={{ borderColor: '#475569' }} />
            </Box>
          ))
        )}

        {notifications.length > 10 && (
          <>
            <Divider sx={{ borderColor: '#475569' }} />
            <Box sx={{ p: 1, textAlign: 'center' }}>
              <Button size="small" sx={{ color: '#60A5FA' }}>
                Ver todas as notificações
              </Button>
            </Box>
          </>
        )}
      </Menu>
    </>
  )
}
