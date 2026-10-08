interface ProductForPost {
    productName: string;
    price: string | number;
    priceDiscountRate?: number;
    offerLink: string;
    commissionRate?: string | number;
}

const EMOJIS = ["🔥", "⚡", "✅", "🎯", "💥", "🛒"];
const HOOKS = [
    "OFERTA IMPERDÍVEL",
    "ACHADO DO DIA",
    "TENDÊNCIA NA SHOPEE",
    "MAIS VENDIDO AGORA",
    "PREÇO BAIXOU",
];

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
