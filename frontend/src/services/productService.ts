import { getData, postData, putData, deleteData } from "./apiResponse";

export interface Product {
    id: number;
    uuid: string;
    item_id: number;
    shop_id: number;
    name: string;
    price: number;
    commission: number;
    score: number;
    confidence: number;
    recommendation: string;
    image: string;
    offer_link: string;
    rating: number;
    sales: number;
    is_active: boolean;
    created_at: string;
    updated_at: string;
    deleted_at: string | null;
}

export interface ProductCreate {
    item_id: number;
    shop_id: number;
    name: string;
    price: number;
    commission: number;
    image: string;
    offer_link: string;
    rating?: number;
    sales?: number;
}

export interface ProductUpdate {
    name?: string;
    price?: number;
    commission?: number;
    image?: string;
    offer_link?: string;
    rating?: number;
    sales?: number;
    score?: number;
    confidence?: number;
    recommendation?: string;
    is_active?: boolean;
}

export async function getProducts(): Promise<Product[]> {
    return getData<Product[]>("/products");
}

export async function getProductById(id: number): Promise<Product> {
    return getData<Product>(`/products/${id}`);
}

export async function createProduct(product: ProductCreate): Promise<Product> {
    return postData<Product, ProductCreate>("/products", product);
}

export async function updateProduct(id: number, product: ProductUpdate): Promise<Product> {
    return putData<Product, ProductUpdate>(`/products/${id}`, product);
}

export async function deleteProduct(id: number): Promise<void> {
    await deleteData<never>(`/products/${id}`);
}
