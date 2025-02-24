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

const getProductImage = (product: Product) => {
  const imageMap: Record<string, string> = {
    // "cheddar cheese": "/products/cheddar.png",
    // "soy milk": "/products/soy-milk.png",
    "kale": "/products/kale.jpg",
    "cucumber": "/products/cucumber.png",
    "eggplant": "/products/eggplant.webp",
    "ginger": "/products/ginger.webp",
    "lemon": "/products/lemon.png",
    "tomato": "/products/tomato.png",
    "swiss cheese": "/products/swiss-cheese.jpg",
    "coffee creamer": "/products/coffee-creamer.jpg",
    "yogurt": "/products/yogurt.jpg",
    "ricotta cheese": "/products/ricotta.jpg",
  };
  return imageMap[product.product_name.toLowerCase()] || null;
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
      getItemImage={getProductImage}
    />
  );
};