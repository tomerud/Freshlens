import { useParams, Link } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";

import { FridgeHeader } from "../fridgeHeader";
import { useSearch } from "../../allFridgesPage/hooks/useSearch";

import "./categoryPage.scss";

interface Product {
    product_id: number;
    product_name: string;
}

const fetchData = async (fridgeId: string, categoryName: string): Promise<Product[]> => {
    const response = await fetch(`/api/get_all_products?fridge_id=${fridgeId}&category_name=${categoryName}`);
    if (!response.ok) throw new Error('Failed to fetch data');
    return await response.json();
};

export const CategoryPage = () => {
    const { fridgeId, categoryName } = useParams<{ fridgeId: string, categoryName: string }>();

    const { data: products = [], isLoading, error } = useQuery<Product[], Error>({
        queryKey: ['products', fridgeId, categoryName],
        queryFn: () => fetchData(fridgeId!, categoryName!),
    });

    const { filteredResults, setSearchQuery } = useSearch(products, 
        (product, query) => product.product_name.toLowerCase().includes(query)
    );

    if (isLoading) return <p>Loading...</p>;
    if (error) return <p>Error: {error.message}</p>;

    return (
        <div>
            <FridgeHeader 
                title={`MY ${categoryName?.toUpperCase()}`} 
                subtitle="Choose a product" 
                onSearch={setSearchQuery} 
            />
            <div className="product-list">
                {filteredResults.length > 0 ? (
                    filteredResults.map((product) => (
                        <Link key={product.product_id} to={`${product.product_id}`} className="product-item">
                            {product.product_name}
                        </Link>
                    ))
                ) : (
                    <p className="no-products">No matching products found.</p>
                )}
            </div>
        </div>
    );
};
