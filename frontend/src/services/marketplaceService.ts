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
    keyword?: string;
    page?: number;
    limit?: number;
    sortType?: number;
}

const MARKETPLACE_TIMEOUT = 10000; // 10s — chamadas externas não devem travar a UI

export async function searchShopeeProducts(filters: MarketplaceFilters): Promise<ShopeeProductResponse> {
    const response = await api.get(
        `/marketplace/products?keyword=${encodeURIComponent(filters.keyword || "")}&page=${filters.page || 1}&limit=${filters.limit || 20}&sortType=${filters.sortType || 1}`,
        { timeout: MARKETPLACE_TIMEOUT }
    );
    return response.data.data as ShopeeProductResponse;
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
