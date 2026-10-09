import api from "../api/axios";

export interface ShopeeProductNode {
    itemId: number;
    productName: string;
    shopName: string;
    shopId: number;
    productLink: string;
    offerLink: string;
    imageUrl: string;
    price: string;
    priceMin: string;
    priceMax: string;
    sales: number;
    commission: string;
    commissionRate: string;
    sellerCommissionRate: string;
    shopeeCommissionRate: string;
    ratingStar: string;
    priceDiscountRate: number;
    productCatIds: number[];
    shopType: number[];
    periodStartTime: number;
    periodEndTime: number;
    score?: number | null;
    decision?: string | null;
    alreadyTracked?: boolean;
    marketplace?: string;
}

export interface PromotePayload {
    item_id: number;
    product_name: string;
    price?: number;
    commission_rate?: number;
    rating_star?: number;
    sales?: number;
    offer_link?: string;
    image_url?: string;
    tone?: string;
}

export interface PromoteResult {
    content: {
        title?: string;
        caption?: string;
        hashtags?: string;
        target_audience?: string;
        channel?: string;
        link?: string;
        ai_generated?: boolean;
    };
    tracking_code: string;
    tracking_url: string;
    full_text: string;
    whatsapp_share_url: string;
    facebook_share_url: string;
}

export async function promoteProduct(payload: PromotePayload): Promise<PromoteResult> {
    const response = await api.post("/marketplace/promote", payload);
    return response.data.data as PromoteResult;
}

export interface ShopeeProductResponse {
    nodes: ShopeeProductNode[];
    pageInfo: {
        page: number | null;
        limit: number;
        hasNextPage: boolean;
        scrollId: string | null;
    };
}

export interface MarketplaceFilters {
    marketplace?: string;
    keyword?: string;
    page?: number;
    limit?: number;
    sortType?: number;
}

// A API da Shopee costuma responder em poucos segundos, mas em buscas
// sem cache (primeira chamada para uma palavra-chave) já foi observado
// levar mais de 10s — por isso o timeout tem folga para não estourar
// antes da resposta chegar e gerar "Erro ao buscar produtos" indevido.
const MARKETPLACE_TIMEOUT = 20000; // 20s — chamadas externas não devem travar a UI

// A busca de catálogo do Mercado Livre varre vários candidatos até achar
// os que têm oferta ativa (pode levar ~9s no backend) — por isso usa um
// timeout maior do que a Shopee para não estourar antes da resposta chegar.
const MARKETPLACE_TIMEOUT_MERCADO_LIVRE = 25000; // 25s

export async function searchShopeeProducts(filters: MarketplaceFilters): Promise<ShopeeProductResponse> {
    const marketplace = filters.marketplace || "shopee";
    const timeout = marketplace === "mercado_livre" ? MARKETPLACE_TIMEOUT_MERCADO_LIVRE : MARKETPLACE_TIMEOUT;
    const response = await api.get(
        `/marketplace/products?marketplace=${encodeURIComponent(marketplace)}&keyword=${encodeURIComponent(filters.keyword || "")}&page=${filters.page || 1}&limit=${filters.limit || 20}&sortType=${filters.sortType || 1}`,
        { timeout }
    );
    const data = response.data.data as ShopeeProductResponse;
    data.nodes = data.nodes.map((node) => ({ ...node, marketplace: node.marketplace || marketplace }));
    return data;
}

export async function searchShopeeShops(filters: MarketplaceFilters): Promise<ShopeeProductResponse> {
    const response = await api.get(
        `/marketplace/shops?keyword=${encodeURIComponent(filters.keyword || "")}&page=${filters.page || 1}&limit=${filters.limit || 20}&sortType=${filters.sortType || 1}`,
        { timeout: MARKETPLACE_TIMEOUT }
    );
    return response.data.data as ShopeeProductResponse;
}

export async function searchShopeeOffers(filters: MarketplaceFilters): Promise<ShopeeProductResponse> {
    const response = await api.get(
        `/marketplace/offers?keyword=${encodeURIComponent(filters.keyword || "")}&page=${filters.page || 1}&limit=${filters.limit || 20}&sortType=${filters.sortType || 1}`,
        { timeout: MARKETPLACE_TIMEOUT }
    );
    return response.data.data as ShopeeProductResponse;
}
