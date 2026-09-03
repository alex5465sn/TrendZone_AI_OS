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
