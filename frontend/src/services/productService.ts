import { getData, postData, putData, deleteData } from "./apiResponse";

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
    return getData<Product[]>("/products");
}

export async function createProduct(product: ProductCreate): Promise<Product> {
    return postData<Product, ProductCreate>("/products", product);
}

export async function updateProduct(id: number, product: ProductCreate): Promise<Product> {
    return putData<Product, ProductCreate>(`/products/${id}`, product);
}

export async function deleteProduct(id: number): Promise<void> {
    await deleteData<never>(`/products/${id}`);
}
