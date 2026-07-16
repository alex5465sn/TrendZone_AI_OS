import api from "../api/axios";

export interface Product {

    id: number;

    item_id: number;

    shop_id: number;

    name: string;

    price: number;

    commission: number;

    score: number;

    image: string;

    offer_link: string;

    rating: number;

    sales: number;

    active: boolean;

}

export interface ProductCreate {

    item_id: number;

    shop_id: number;

    name: string;

    price: number;

    commission: number;

    image: string;

    offer_link: string;

}

export async function getProducts(): Promise<Product[]> {

    const response = await api.get<Product[]>("/products");

    return response.data;

}

export async function createProduct(
    product: ProductCreate,
): Promise<Product> {

    const response = await api.post<Product>(
        "/products",
        product,
    );

    return response.data;

}

export async function updateProduct(
    id: number,
    product: ProductCreate,
): Promise<Product> {

    const response = await api.put<Product>(
        `/products/${id}`,
        product,
    );

    return response.data;

}

export async function deleteProduct(
    id: number,
): Promise<void> {

    await api.delete(`/products/${id}`);

}