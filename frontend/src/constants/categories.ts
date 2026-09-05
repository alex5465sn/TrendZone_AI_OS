export interface CategoryDef {
    id: string;
    label: string;
    keywords: string[];
}

export const CATEGORIES: CategoryDef[] = [
    { id: "eletronicos", label: "Eletrônicos", keywords: ["fone de ouvido", "carregador rapido", "power bank", "caixa de som bluetooth"] },
    { id: "casa", label: "Casa e Decoração", keywords: ["organizador multiuso", "luminaria led", "utensilio de cozinha"] },
    { id: "beleza", label: "Beleza e Cuidados", keywords: ["kit skincare", "escova secadora", "perfume importado"] },
    { id: "pet", label: "Pet Shop", keywords: ["brinquedo para cachorro", "comedouro automatico pet", "coleira para gato"] },
    { id: "tecnologia", label: "Tecnologia e Acessórios", keywords: ["suporte para celular", "smartwatch", "capa para celular"] },
    { id: "moda", label: "Moda e Acessórios", keywords: ["oculos de sol", "bolsa feminina", "relogio masculino"] },
    { id: "bebe", label: "Bebê e Infantil", keywords: ["brinquedo educativo", "mochila infantil"] },
    { id: "esporte", label: "Esporte e Fitness", keywords: ["faixa elastica", "garrafa de agua esportiva", "luva de treino"] },
    { id: "automotivo", label: "Automotivo", keywords: ["organizador de carro", "suporte veicular celular"] },
    { id: "papelaria", label: "Papelaria e Escritório", keywords: ["caderno inteligente", "kit escritorio organizador"] },
];

export function getKeywordsForCategories(categoryIds: string[]): string[] {
    if (categoryIds.length === 0) {
        return CATEGORIES.flatMap((c) => c.keywords);
    }
    return CATEGORIES.filter((c) => categoryIds.includes(c.id)).flatMap((c) => c.keywords);
}
