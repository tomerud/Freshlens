import _ from "lodash";
import { useParams } from "react-router-dom";

import { Options } from "../../options";

import "./categoryPage.scss";

interface Product {
    product_id: number;
    product_name: string;
  }
  
  const fetchProducts = async (fridgeId: string, categoryName: string): Promise<Product[]> => {
    const response = await fetch(`/api/get_all_products?fridge_id=${fridgeId}&category_name=${categoryName}`);
    if (!response.ok) throw new Error("Failed to fetch data");
    return response.json();
  };
  
  export const CategoryPage = () => {
    const { fridgeId, categoryName } = useParams<{ fridgeId: string; categoryName: string }>();
  
    return (
      <Options
        title={`MY ${categoryName}`}
        subtitle="Choose a product"
        queryKey={["products", fridgeId, categoryName]}
        queryFn={() => fetchProducts(fridgeId!, categoryName!)}
        filterFn={(product, query) => product.product_name.toLowerCase().includes(query)}
        itemKey={(product) => product.product_id}
        itemLabel={(product) => product.product_name}
        itemLink={(product) => `${product.product_id}`}
      />
    );
  };
