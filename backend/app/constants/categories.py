"""
TrendZone AI OS
================================

Categorias oficiais da Shopee.

Fonte: taxonomia de categorias exibida
no app/site da Shopee (fornecida pelo usuário).

Cada categoria tem uma ou mais palavras-chave
de busca associadas, usadas pelo AutoScoutService
para alimentar o catálogo automaticamente e pela
API de busca de produtos para permitir filtro por
categoria.

"Shopee Doações" fica de fora da rotação automática
de busca (não é uma categoria de produto de afiliado),
mas permanece na lista para fins de exibição/filtro.
"""

CATEGORIES: dict[str, dict[str, list[str]]] = {
    "roupas_femininas": {"label": "Roupas Femininas", "keywords": ["vestido feminino", "blusa feminina"]},
    "casa_construcao": {"label": "Casa e Construção", "keywords": ["organizador multiuso", "ferramenta manual"]},
    "roupas_plus_size": {"label": "Roupas Plus Size", "keywords": ["roupa plus size feminina"]},
    "beleza": {"label": "Beleza", "keywords": ["kit skincare", "perfume importado"]},
    "roupas_masculinas": {"label": "Roupas Masculinas", "keywords": ["camisa masculina", "bermuda masculina"]},
    "sapatos_femininos": {"label": "Sapatos Femininos", "keywords": ["sandalia feminina", "tenis feminino"]},
    "sapatos_masculinos": {"label": "Sapatos Masculinos", "keywords": ["tenis masculino", "sapato social masculino"]},
    "moda_infantil": {"label": "Moda Infantil", "keywords": ["roupa infantil menino", "roupa infantil menina"]},
    "acessorios_moda": {"label": "Acessórios de Moda", "keywords": ["oculos de sol", "cinto de couro"]},
    "relogios": {"label": "Relógios", "keywords": ["relogio masculino", "relogio feminino"]},
    "celulares_dispositivos": {"label": "Celulares e Dispositivos", "keywords": ["capa para celular", "pelicula celular"]},
    "esportes_lazer": {"label": "Esportes e Lazer", "keywords": ["faixa elastica", "garrafa de agua esportiva"]},
    "eletrodomesticos": {"label": "Eletrodomésticos", "keywords": ["air fryer", "liquidificador"]},
    "brinquedos_hobbies": {"label": "Brinquedos e Hobbies", "keywords": ["brinquedo educativo", "quebra cabeca"]},
    "automoveis": {"label": "Automóveis", "keywords": ["acessorio para carro", "organizador de carro"]},
    "acessorios_veiculos": {"label": "Acessórios para Veículos", "keywords": ["suporte veicular celular", "tapete automotivo"]},
    "saude": {"label": "Saúde", "keywords": ["vitamina suplemento", "termometro digital"]},
    "motocicletas": {"label": "Motocicletas", "keywords": ["capacete moto", "acessorio para moto"]},
    "audio": {"label": "Áudio", "keywords": ["fone de ouvido", "caixa de som bluetooth"]},
    "mae_bebe": {"label": "Mãe e Bebê", "keywords": ["fralda descartavel", "mochila maternidade"]},
    "bolsas_femininas": {"label": "Bolsas Femininas", "keywords": ["bolsa feminina transversal"]},
    "bolsas_masculinas": {"label": "Bolsas Masculinas", "keywords": ["mochila masculina"]},
    "animais_domesticos": {"label": "Animais Domésticos", "keywords": ["brinquedo para cachorro", "coleira para gato"]},
    "papelaria": {"label": "Papelaria", "keywords": ["caderno inteligente", "kit escritorio organizador"]},
    "computadores_acessorios": {"label": "Computadores e Acessórios", "keywords": ["teclado mecanico", "mouse gamer"]},
    "alimentos_bebidas": {"label": "Alimentos e Bebidas", "keywords": ["cafe gourmet", "chocolate importado"]},
    "jogos_consoles": {"label": "Jogos e Consoles", "keywords": ["controle joystick", "acessorio video game"]},
    "cameras_drones": {"label": "Câmeras e Drones", "keywords": ["mini camera", "drone com camera"]},
    "viagens_bagagens": {"label": "Viagens e Bagagens", "keywords": ["mala de viagem", "organizador de mala"]},
    "livros_revistas": {"label": "Livros e Revistas", "keywords": ["livro best seller"]},
    "shopee_doacoes": {"label": "Shopee Doações", "keywords": []},
}


def get_keyword_rotation() -> list[tuple[str, str]]:
    """
    Retorna pares (categoria, palavra-chave) para o
    AutoScoutService rotacionar — ignora categorias
    sem palavras-chave de busca (ex: Shopee Doações).
    """
    pairs: list[tuple[str, str]] = []
    for category_id, data in CATEGORIES.items():
        for keyword in data["keywords"]:
            pairs.append((category_id, keyword))
    return pairs


def keyword_to_category(keyword: str) -> str:
    """
    Tenta identificar a categoria de um produto a partir
    da palavra-chave usada na busca. Se não encontrar,
    retorna "geral".
    """
    keyword_lower = (keyword or "").strip().lower()
    for category_id, data in CATEGORIES.items():
        if keyword_lower in [k.lower() for k in data["keywords"]]:
            return category_id
    return "geral"
