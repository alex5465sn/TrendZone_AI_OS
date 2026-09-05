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

function pick<T>(arr: T[]): T {
    return arr[Math.floor(Math.random() * arr.length)];
}

export function generateFacebookPost(product: ProductForPost): string {

    const emoji = pick(EMOJIS);
    const hook = pick(HOOKS);
    const discount = product.priceDiscountRate ? `${product.priceDiscountRate}% OFF` : "";
    const price = typeof product.price === "number" ? product.price.toFixed(2) : product.price;

    const lines = [
        `${emoji} ${hook}: ${product.productName}`,
        "",
        `💰 Por apenas R$ ${price} ${discount ? `(${discount})` : ""}`.trim(),
        "",
        "📦 Envio rápido pela Shopee",
        "🔗 Link na Shopee (compra 100% segura):",
        product.offerLink,
        "",
        "👉 Corre que estoque é limitado!",
        "",
        "#shopee #promocao #achadosdodia #trendzone",
    ];

    return lines.join("\n");
}
