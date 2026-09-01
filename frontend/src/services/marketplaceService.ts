import { getData } from "./apiResponse";

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

export async function searchShopeeProducts(filters: MarketplaceFilters): Promise<ShopeeProductResponse> {
    return getData<ShopeeProductResponse>(`/marketplace/products?keyword=${encodeURIComponent(filters.keyword || "")}&page=${filters.page || 1}&limit=${filters.limit || 20}&sortType=${filters.sortType || 1}`);
}

export async function searchShopeeShops(filters: MarketplaceFilters): Promise<ShopeeProductResponse> {
    return getData<ShopeeProductResponse>(`/marketplace/shops?keyword=${encodeURIComponent(filters.keyword || "")}&page=${filters.page || 1}&limit=${filters.limit || 20}&sortType=${filters.sortType || 1}`);
}

export async function searchShopeeOffers(filters: MarketplaceFilters): Promise<ShopeeProductResponse> {
    return getData<ShopeeProductResponse>(`/marketplace/offers?keyword=${encodeURIComponent(filters.keyword || "")}&page=${filters.page || 1}&limit=${filters.limit || 20}&sortType=${filters.sortType || 1}`);
}
