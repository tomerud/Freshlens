import { useQuery } from "@tanstack/react-query";
import { useParams } from "react-router-dom";

import { Loader } from "../../../../../loader";

import "./nutrientData.scss";

interface ProductNutrientData {
  product_name: string;
  serving_size: string | null;
  energy_kcal: number | null;
  protein_g: number | null;
  fat_g: number | null;
  saturated_fat_g: number | null;
  carbs_g: number | null;
  sugars_g: number | null;
  fiber_g: number | null;
  sodium_mg: number | null;
}

const fetchData = async (productId: string): Promise<ProductNutrientData> => {
  const response = await fetch(`/api/get_product_nutrient?product_id=${productId}`);

  if (!response.ok) {
    throw new Error("Failed to fetch data");
  }

  return await response.json();
};

export const NutrientData = () => {
  const { productId } = useParams<{ productId: string }>();

  const { data: nutrientData, isLoading, error } = useQuery<ProductNutrientData, Error>({
    queryKey: ["nutrientData", productId],
    queryFn: () => fetchData(productId!),
  });

  if (isLoading) return <Loader />;
  if (error) return <div>Error: {error.message}</div>;

  return (
    <div className="nutrient-container">
      <h2 className="nutrient-title">Nutriant Values</h2>
      <span className="fridge-subtext">per 100gr</span>
      <p className="serving-size">
      </p>

      <table className="nutrient-table">
        <thead>
          <tr>
            <th>Nutrient</th>
            <th>Value</th>
            <th>Unit</th>
          </tr>
        </thead>
        <tbody>
          {[
            ["Energy", nutrientData?.energy_kcal, "KCAL"],
            ["Protein", nutrientData?.protein_g, "G"],
            ["Total Fat", nutrientData?.fat_g, "G"],
            ["Saturated Fat", nutrientData?.saturated_fat_g, "G"],
            ["Carbohydrates", nutrientData?.carbs_g, "G"],
            ["Sugars", nutrientData?.sugars_g, "G"],
            ["Fiber", nutrientData?.fiber_g, "G"],
            ["Sodium", nutrientData?.sodium_mg, "MG"],
          ].map(([key, value, unit]) => (
            <tr key={key}>
              <td>{key}</td>
              <td>{value !== null ? value : "N/A"}</td>
              <td>{unit}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};
