import { useQuery } from "@tanstack/react-query";
import { motion } from "framer-motion";

import { Loader } from "../../../loader";
import { useAuth } from "../../../../contexts/userContext";

import "./recipeSuggestion.scss";


interface RecipeResponse {
  recipe: string;
}

const fetchRecipe = async (userId: string): Promise<RecipeResponse> => {
  const response = await fetch(`/api/get_suggested_recipe?user_id=${userId}`);

  if (!response.ok) {
    throw new Error("Failed to fetch recipe");
  }

  return await response.json();
};

export const RecipeSuggestion = () => {
  // const { user } = useAuth();
  const userId = "0NNRFLhbXJRFk3ER2_iTr8VulFm4";
  // const { data, isLoading, error } = useQuery<RecipeResponse, Error>({
  //   queryKey: ["recipeSuggestion", userId],
  //   queryFn: () => fetchRecipe(userId),
  // });

  // if (isLoading) return <Loader />;
  // if (error) return <p className="error-message">Error: {error.message}</p>;
  // if (!data?.recipe) return <p className="no-recipe">No recipe for today</p>;

  const recipe = "khrjg gshgkj hg jhg ks"
  return (
    <motion.div
      className="recipe-container"
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <h3 className="recipe-title">Suggested Recipe</h3>
      <p className="recipe-text">{recipe}</p> 
    </motion.div>
  );
};
