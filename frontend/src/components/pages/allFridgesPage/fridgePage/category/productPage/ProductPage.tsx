import { useParams } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { FridgeHeader } from "../../../fridgeHeader";
import { ItemsList } from "./ItemsList";
import { Loader } from "../../../../../loader";
import { PriceData } from "./PriceData";
import { NutrientData } from "./NutrientData";
import { TipsSection } from "../../../../../TipsSection";

import "./productPage.scss";


interface Product {
  product_id: string;
  product_name: string;
}

const fetchData = async (productId: string): Promise<Product> => {
  const response = await fetch(`/api/get_product_name?product_id=${productId}`);

  if (!response.ok) {
    throw new Error("Failed to fetch data");
  }

  return await response.json();
};

export const ProductPage = () => {
  const { productId } = useParams<{ productId: string }>();

  const { data: ProductName, isLoading, error } = useQuery<Product, Error>({
    queryKey: ["ProductName", productId],
    queryFn: () => fetchData(productId!),
  });

  if (isLoading) return <Loader />;
  if (error) return <div>Error: {error.message}</div>;
  
  return (
    <>
      <FridgeHeader title={ProductName!.product_name} subtitle="everything you want to know"/>
      <ItemsList />
      <NutrientData />
      <PriceData/>
      <TipsSection productId={productId} addedTitle={ProductName!.product_name} classname="no-border"/>
    </>
  );
};
