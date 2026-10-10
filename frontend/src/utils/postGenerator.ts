interface ProductForPost {
    productName: string;
    price: string | number;
    priceDiscountRate?: number;
    offerLink: string;
    commissionRate?: string | number;
}

/**
 * Ângulos estruturados de criativo (Fase 2 do Product Hunter)
 * Cada ângulo resolve um problema diferente de persuasão
 */
export const CreativeAngle = {
    PROBLEM: "problem",
    TRANSFORMATION: "transformation",
    THREE_REASONS: "three_reasons",
    DEMONSTRATION: "demonstration",
    COMPARISON: "comparison",
} as const;

export type CreativeAngle = typeof CreativeAngle[keyof typeof CreativeAngle];

const EMOJIS = ["🔥", "⚡", "✅", "🎯", "💥", "🛒"];
const HOOKS = [
    "OFERTA IMPERDÍVEL",
    "ACHADO DO DIA",
    "TENDÊNCIA NA SHOPEE",
    "MAIS VENDIDO AGORA",
    "PREÇO BAIXOU",
];

// =====================================================
// ÂNGULOS ESTRUTURADOS (Fase 2)
// =====================================================

const ANGLE_HOOKS: Record<CreativeAngle, string[]> = {
    [CreativeAngle.PROBLEM]: [
        "Se você sofre com isso, achei a solução",
        "Cansado de lidar com esse problema?",
        "Você ainda está fazendo isso do jeito antigo?",
        "Esse problema te custa tempo e dinheiro",
    ],
    [CreativeAngle.TRANSFORMATION]: [
        "Veja a transformação que isso faz",
        "Antes e depois que vai te surpreender",
        "De bagunçado para perfeito em segundos",
        "A mudança que você não sabia que precisava",
    ],
    [CreativeAngle.THREE_REASONS]: [
        "3 motivos para ter isso em casa",
        "Por que todo mundo está comprando",
        "3 razões que vão te convencer",
        "Descubra por que é tão procurado",
    ],
    [CreativeAngle.DEMONSTRATION]: [
        "Veja como funciona na prática",
        "Demonstração rápida do resultado",
        "Assim é fácil entender por que vende",
        "Funcionamento que fala por si só",
    ],
    [CreativeAngle.COMPARISON]: [
        "Comparado com alternativas, é imbatível",
        "Melhor que as opções caras",
        "Qualidade por uma fração do preço",
        "Vs. produtos similares: ganha fácil",
    ],
};

const ANGLE_BODIES: Record<CreativeAngle, string[]> = {
    [CreativeAngle.PROBLEM]: [
        "Muita gente sofre com isso diariamente. Mas existe uma solução simples que resolve 100%.",
        "O problema é comum, mas a maioria não sabe que existe algo tão eficaz.",
        "Você não está sozinho. Milhares já descobriram como resolver isso.",
    ],
    [CreativeAngle.TRANSFORMATION]: [
        "Veja só a diferença que faz. Antes era caos, agora é organizado.",
        "A transformação é tão visível que parece mágica.",
        "Resultado que você consegue em minutos, não em horas.",
    ],
    [CreativeAngle.THREE_REASONS]: [
        "1️⃣ Resolve o problema de verdade\n2️⃣ Preço que cabe no bolso\n3️⃣ Qualidade comprovada",
        "1️⃣ Funciona melhor que alternativas\n2️⃣ Dura muito tempo\n3️⃣ Fácil de usar",
        "1️⃣ Economiza seu tempo\n2️⃣ Economiza seu dinheiro\n3️⃣ Muda sua rotina",
    ],
    [CreativeAngle.DEMONSTRATION]: [
        "Coloca aqui → resultado ali. Simples assim.",
        "Funciona tão bem que parece que foi feito só para isso.",
        "A demonstração fala mais que mil palavras.",
    ],
    [CreativeAngle.COMPARISON]: [
        "Produtos similares custam 3x mais. Esse faz a mesma coisa.",
        "Qualidade de marca cara, preço de promoção.",
        "Você pagaria mais caro em outro lugar. Aqui é mais barato.",
    ],
};

// Variações de CTA e corpo, para que cada post gerado para o mesmo produto
// não saia idêntico ao anterior — evita a aparência de "spam" (texto
// repetido) ao divulgar o mesmo produto em grupos/redes diferentes.
const BODY_STYLES: Array<(discount: string) => string> = [
    (discount) => `📦 Envio rápido pela Shopee\n🔗 Link na Shopee (compra 100% segura):${discount ? `\n🏷️ ${discount} só hoje` : ""}`,
    (discount) => `✅ Avaliado por quem já comprou\n🔗 Garanta o seu antes que acabe:${discount ? `\n💸 ${discount} por tempo limitado` : ""}`,
    (discount) => `🚚 Chega rapidinho aí na sua casa\n🔗 Compra 100% segura pela Shopee:${discount ? `\n🔖 ${discount} aplicado` : ""}`,
];

const CTA_STYLES = [
    "👉 Corre que estoque é limitado!",
    "👉 Comenta 'EU QUERO' que eu te mando o link!",
    "👉 Clica agora antes que o preço volte a subir!",
    "👉 Salva esse post e já aproveita o desconto!",
];

function pick<T>(arr: T[]): T {
    return arr[Math.floor(Math.random() * arr.length)];
}

function buildPost(product: ProductForPost, emoji: string, hook: string, bodyIndex: number, cta: string): string {
    const discount = product.priceDiscountRate ? `${product.priceDiscountRate}% OFF` : "";
    const price = typeof product.price === "number" ? product.price.toFixed(2) : product.price;

    const lines = [
        `${emoji} ${hook}: ${product.productName}`,
        "",
        `💰 Por apenas R$ ${price} ${discount ? `(${discount})` : ""}`.trim(),
        "",
        BODY_STYLES[bodyIndex](discount),
        product.offerLink,
        "",
        cta,
        "",
        "#shopee #promocao #achadosdodia #trendzone",
    ];

    return lines.join("\n");
}

export function generateFacebookPost(product: ProductForPost): string {
    return buildPost(product, pick(EMOJIS), pick(HOOKS), Math.floor(Math.random() * BODY_STYLES.length), pick(CTA_STYLES));
}

/**
 * Gera várias variações distintas (hook, corpo e CTA diferentes) do mesmo
 * post, para divulgar o mesmo produto em canais/grupos diferentes sem
 * repetir o texto literalmente.
 */
export function generateFacebookPostVariations(product: ProductForPost, count = 3): string[] {
    const variations: string[] = [];
    const usedHooks = new Set<number>();

    for (let i = 0; i < count; i++) {
        let hookIndex = Math.floor(Math.random() * HOOKS.length);
        if (usedHooks.size < HOOKS.length) {
            while (usedHooks.has(hookIndex)) {
                hookIndex = Math.floor(Math.random() * HOOKS.length);
            }
        }
        usedHooks.add(hookIndex);

        const bodyIndex = i % BODY_STYLES.length;
        const cta = CTA_STYLES[i % CTA_STYLES.length];
        const emoji = EMOJIS[i % EMOJIS.length];

        variations.push(buildPost(product, emoji, HOOKS[hookIndex], bodyIndex, cta));
    }

    return variations;
}

/**
 * Gera 5 criativos estruturados com ângulos diferentes (Fase 2)
 * Cada ângulo é otimizado para um tipo diferente de persuasão
 */
export function generateStructuredCreatives(product: ProductForPost): Record<CreativeAngle, string> {
    const angles = Object.values(CreativeAngle);
    const creatives: Record<CreativeAngle, string> = {} as Record<CreativeAngle, string>;

    for (const angle of angles) {
        const hooks = ANGLE_HOOKS[angle];
        const bodies = ANGLE_BODIES[angle];
        const hook = hooks[Math.floor(Math.random() * hooks.length)];
        const body = bodies[Math.floor(Math.random() * bodies.length)];
        const cta = CTA_STYLES[Math.floor(Math.random() * CTA_STYLES.length)];
        const emoji = EMOJIS[Math.floor(Math.random() * EMOJIS.length)];

        const price = typeof product.price === "number" ? product.price.toFixed(2) : product.price;
        const discount = product.priceDiscountRate ? `${product.priceDiscountRate}% OFF` : "";

        const lines = [
            `${emoji} ${hook}`,
            "",
            `📦 ${product.productName}`,
            `💰 R$ ${price} ${discount ? `(${discount})` : ""}`.trim(),
            "",
            body,
            "",
            product.offerLink,
            "",
            cta,
            "",
            "#shopee #promocao #achadosdodia #trendzone",
        ];

        creatives[angle] = lines.join("\n");
    }

    return creatives;
}
