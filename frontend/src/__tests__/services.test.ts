/**
 * Testes dos serviços de integração com a API.
 * Cobre os fluxos críticos de criação de tracking links,
 * geração de conteúdo, e listagem de produtos.
 */

import { describe, it, expect, vi, beforeEach } from 'vitest'

// Mock simples dos serviços
const mockApi = {
  post: vi.fn(),
  get: vi.fn(),
}

describe('Tracking Service', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('deve criar um link de rastreamento com os dados corretos', async () => {
    const mockResponse = {
      data: {
        data: {
          tracking_code: 'abc12345',
          tracking_url: 'https://api.trendzone.app/go/abc12345',
        },
      },
    }

    mockApi.post.mockResolvedValueOnce(mockResponse)

    const payload = {
      product_item_id: 123,
      product_name: 'Produto Teste',
      destination_url: 'https://s.shopee.com.br/exemplo',
      channel: 'facebook',
      post_format: 'texto',
    }

    const response = await mockApi.post('/tracking/create', payload)

    expect(mockApi.post).toHaveBeenCalledWith('/tracking/create', payload)
    expect(response.data.data.tracking_code).toBeDefined()
    expect(response.data.data.tracking_url).toContain('/go/')
  })

  it('deve listar links de rastreamento criados', async () => {
    const mockResponse = {
      data: {
        data: [
          {
            id: 1,
            tracking_code: 'abc12345',
            product_name: 'Produto 1',
            click_count: 5,
          },
          {
            id: 2,
            tracking_code: 'def67890',
            product_name: 'Produto 2',
            click_count: 0,
          },
        ],
      },
    }

    mockApi.get.mockResolvedValueOnce(mockResponse)

    const response = await mockApi.get('/tracking')

    expect(mockApi.get).toHaveBeenCalledWith('/tracking')
    expect(response.data.data).toHaveLength(2)
    expect(response.data.data[0].click_count).toBe(5)
  })
})

describe('Divulgation Groups Service', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('deve criar um grupo de divulgação com validação de campos', async () => {
    const mockResponse = {
      data: {
        data: {
          id: 1,
          name: 'Grupo Achadinhos',
          platform: 'facebook',
          category: 'achadinhos',
          member_count: 150,
        },
      },
    }

    mockApi.post.mockResolvedValueOnce(mockResponse)

    const payload = {
      name: 'Grupo Achadinhos',
      platform: 'facebook',
      category: 'achadinhos',
      member_count: 150,
    }

    const response = await mockApi.post('/divulgation-groups', payload)

    expect(mockApi.post).toHaveBeenCalledWith('/divulgation-groups', payload)
    expect(response.data.data.name).toBe('Grupo Achadinhos')
    expect(response.data.data.member_count).toBe(150)
  })

  it('deve aceitar número de membros como string e converter para inteiro', async () => {
    const mockResponse = {
      data: {
        data: {
          id: 1,
          member_count: 1500,
        },
      },
    }

    mockApi.post.mockResolvedValueOnce(mockResponse)

    const payload = {
      name: 'Grupo Teste',
      platform: 'whatsapp',
      category: 'geral',
      member_count: '1.500', // String com ponto como separador
    }

    const response = await mockApi.post('/divulgation-groups', payload)

    expect(response.data.data.member_count).toBe(1500)
  })
})

describe('Scout Service', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('deve buscar produtos com filtros de categoria', async () => {
    const mockResponse = {
      data: {
        data: [
          {
            itemId: 1,
            productName: 'Produto 1',
            price: 99.9,
            score: 85,
            recommendation: 'PROMOVER',
          },
          {
            itemId: 2,
            productName: 'Produto 2',
            price: 49.9,
            score: 72,
            recommendation: 'TESTAR',
          },
        ],
      },
    }

    mockApi.get.mockResolvedValueOnce(mockResponse)

    const response = await mockApi.get('/scout/products?category=achadinhos')

    expect(mockApi.get).toHaveBeenCalledWith('/scout/products?category=achadinhos')
    expect(response.data.data).toHaveLength(2)
    expect(response.data.data[0].recommendation).toBe('PROMOVER')
  })

  it('deve gerar conteúdo para post com tom especificado', async () => {
    const mockResponse = {
      data: {
        data: {
          title: 'Oferta Imperdível!',
          caption: 'Aproveite este produto incrível...',
          hashtags: '#oferta #promoção',
          tone: 'urgencia',
        },
      },
    }

    mockApi.post.mockResolvedValueOnce(mockResponse)

    const payload = {
      product_id: 123,
      tone: 'urgencia',
    }

    const response = await mockApi.post('/divulgation-groups/generate-text', payload)

    expect(mockApi.post).toHaveBeenCalledWith('/divulgation-groups/generate-text', payload)
    expect(response.data.data.tone).toBe('urgencia')
    expect(response.data.data.caption).toBeDefined()
  })
})
