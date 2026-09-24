export interface CategoryDef {
    id: string;
    label: string;
    keywords: string[];
}

// Taxonomia oficial de categorias da Shopee (Brasil).
// Usada na tela de Prospecção, no filtro de Produtos
// e espelhada no backend em app/constants/categories.py
// para manter a mesma classificação em toda a plataforma.
export const CATEGORIES: CategoryDef[] = [
    { id: "roupas_femininas", label: "Roupas Femininas", keywords: ["vestido feminino", "blusa feminina"] },
    { id: "casa_construcao", label: "Casa e Construção", keywords: ["organizador multiuso", "luminaria led", "utensilio de cozinha"] },
    { id: "roupas_plus_size", label: "Roupas Plus Size", keywords: ["roupa plus size", "vestido plus size"] },
    { id: "beleza", label: "Beleza", keywords: ["kit skincare", "perfume importado"] },
    { id: "roupas_masculinas", label: "Roupas Masculinas", keywords: ["camisa masculina", "bermuda masculina"] },
    { id: "sapatos_femininos", label: "Sapatos Femininos", keywords: ["sapato feminino", "sandalia feminina"] },
    { id: "sapatos_masculinos", label: "Sapatos Masculinos", keywords: ["tenis masculino", "sapato masculino"] },
    { id: "moda_infantil", label: "Moda Infantil", keywords: ["roupa infantil", "mochila infantil"] },
    { id: "acessorios_moda", label: "Acessórios de Moda", keywords: ["oculos de sol", "cinto"] },
    { id: "relogios", label: "Relógios", keywords: ["relogio masculino", "relogio feminino"] },
    { id: "celulares_dispositivos", label: "Celulares e Dispositivos", keywords: ["capa para celular", "carregador rapido"] },
    { id: "esportes_lazer", label: "Esportes e Lazer", keywords: ["faixa elastica", "garrafa de agua esportiva"] },
    { id: "eletrodomesticos", label: "Eletrodomésticos", keywords: ["air fryer", "liquidificador"] },
    { id: "brinquedos_hobbies", label: "Brinquedos e Hobbies", keywords: ["brinquedo educativo", "quebra cabeca"] },
    { id: "automoveis", label: "Automóveis", keywords: ["organizador de carro", "acessorio automotivo"] },
    { id: "acessorios_veiculos", label: "Acessórios para Veículos", keywords: ["suporte veicular celular", "capa de banco"] },
    { id: "saude", label: "Saúde", keywords: ["suplemento vitaminico", "massageador"] },
    { id: "motocicletas", label: "Motocicletas", keywords: ["capacete moto", "acessorio moto"] },
    { id: "audio", label: "Áudio", keywords: ["fone de ouvido", "caixa de som bluetooth"] },
    { id: "mae_bebe", label: "Mãe e Bebê", keywords: ["fralda", "carrinho de bebe"] },
    { id: "bolsas_femininas", label: "Bolsas Femininas", keywords: ["bolsa feminina", "carteira feminina"] },
    { id: "bolsas_masculinas", label: "Bolsas Masculinas", keywords: ["mochila masculina", "pasta masculina"] },
    { id: "animais_domesticos", label: "Animais Domésticos", keywords: ["brinquedo para cachorro", "comedouro automatico pet"] },
    { id: "papelaria", label: "Papelaria", keywords: ["caderno inteligente", "kit escritorio organizador"] },
    { id: "computadores_acessorios", label: "Computadores e Acessórios", keywords: ["teclado mecanico", "mouse gamer"] },
    { id: "alimentos_bebidas", label: "Alimentos e Bebidas", keywords: ["cafe gourmet", "snack saudavel"] },
    { id: "jogos_consoles", label: "Jogos e Consoles", keywords: ["controle de video game", "jogo para console"] },
    { id: "cameras_drones", label: "Câmeras e Drones", keywords: ["camera de acao", "drone com camera"] },
    { id: "viagens_bagagens", label: "Viagens e Bagagens", keywords: ["mala de viagem", "mochila de viagem"] },
    { id: "livros_revistas", label: "Livros e Revistas", keywords: ["livro best seller", "revista em quadrinhos"] },
    { id: "shopee_doacoes", label: "Shopee Doações", keywords: [] },
];

export function getKeywordsForCategories(categoryIds: string[]): string[] {
    if (categoryIds.length === 0) {
        return CATEGORIES.flatMap((c) => c.keywords);
    }
    return CATEGORIES.filter((c) => categoryIds.includes(c.id)).flatMap((c) => c.keywords);
}
