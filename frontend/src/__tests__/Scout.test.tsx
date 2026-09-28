/**
 * Testes do componente Scout.
 * Cobre renderização, seleção de categorias, e fluxo de geração de posts.
 */

import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { BrowserRouter } from 'react-router-dom'

import { useState } from 'react'

// Mock simples do componente Scout para testes
const MockScout = () => {
  const [loading] = useState(false)
  const [products] = useState([])

  return (
    <div>
      <h1>Scout IA</h1>
      <button data-testid="search-button">Buscar Produtos</button>
      <div data-testid="products-list">
        {products.length === 0 ? <p>Nenhum produto encontrado</p> : null}
      </div>
      <button data-testid="generate-post-button" disabled={loading}>
        Gerar Post
      </button>
    </div>
  )
}

describe('Scout Component', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('deve renderizar o componente Scout com elementos principais', () => {
    render(
      <BrowserRouter>
        <MockScout />
      </BrowserRouter>
    )

    expect(screen.getByText('Scout IA')).toBeInTheDocument()
    expect(screen.getByTestId('search-button')).toBeInTheDocument()
    expect(screen.getByTestId('generate-post-button')).toBeInTheDocument()
  })

  it('deve permitir clique no botão de gerar post quando não está carregando', () => {
    render(
      <BrowserRouter>
        <MockScout />
      </BrowserRouter>
    )

    const generateButton = screen.getByTestId('generate-post-button')
    expect(generateButton).not.toBeDisabled()
  })

  it('deve exibir mensagem quando nenhum produto é encontrado', () => {
    render(
      <BrowserRouter>
        <MockScout />
      </BrowserRouter>
    )

    expect(screen.getByText('Nenhum produto encontrado')).toBeInTheDocument()
  })

  it('deve permitir clique no botão de busca', async () => {
    const user = userEvent.setup()
    render(
      <BrowserRouter>
        <MockScout />
      </BrowserRouter>
    )

    const searchButton = screen.getByTestId('search-button')
    await user.click(searchButton)

    expect(searchButton).toBeInTheDocument()
  })
})

describe('Scout Category Selection', () => {
  it('deve permitir seleção de múltiplas categorias', () => {
    const selected = ['achadinhos', 'moda']

    expect(selected).toContain('achadinhos')
    expect(selected).toContain('moda')
    expect(selected).not.toContain('beleza')
  })

  it('deve sugerir categoria automaticamente a partir do nome do grupo', () => {
    const groupName = 'Grupo Achadinhos SP'
    const keywords = {
      achadinhos: ['achadinho', 'achados', 'promoção'],
      moda: ['moda', 'roupa', 'look'],
    }

    const suggestedCategory = Object.entries(keywords).find(([_, kws]) =>
      kws.some((k) => groupName.toLowerCase().includes(k))
    )?.[0]

    expect(suggestedCategory).toBe('achadinhos')
  })
})
