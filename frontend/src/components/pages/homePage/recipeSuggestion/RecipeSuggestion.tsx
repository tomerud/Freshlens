import { useQuery } from "@tanstack/react-query";
import { motion } from "framer-motion";

import { Loader } from "../../../loader";
import { useAuth } from "../../../../contexts/userContext";

import "./recipeSuggestion.scss";


interface RecipeResponse {
  recipes: string;
}


const splitRecipes = (recipeString: string) => {
  const rawRecipes = recipeString.split("###").map(recipe => recipe.trim()).filter(recipe => recipe.length > 0);

  return rawRecipes.map(recipeText => {
    const titleMatch = recipeText.match(/Recipe \d+:\s*(.*)/);
    const title = titleMatch ? titleMatch[1].trim() : "Unknown Recipe";

    const ingredientsMatch = recipeText.match(/Ingredients:\n([\s\S]*?)\n\nInstructions:/);
    const ingredients = ingredientsMatch 
      ? ingredientsMatch[1].split("\n").map(line => line.trim()).filter(line => line.startsWith("-")) 
      : [];

    const instructionsMatch = recipeText.match(/Instructions:\n([\s\S]*)/);
    const instructions = instructionsMatch 
      ? instructionsMatch[1].split("\n").map(line => line.trim()).filter(line => line.length > 0) 
      : [];

    return { title, ingredients, instructions };
  });
};

const fetchRecipe = async (userId: string): Promise<RecipeResponse> => {
  const response = await fetch(`/api/get_suggested_recipe?fridge_id=${1}`);

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

  // const a = splitRecipes(data.recipes)
  // console.log(a);

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
