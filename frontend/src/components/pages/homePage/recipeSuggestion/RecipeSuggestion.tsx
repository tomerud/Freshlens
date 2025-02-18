import { useQuery } from "@tanstack/react-query";
import { motion } from "framer-motion";

import { Loader } from "../../../loader";
import { useAuth } from "../../../../contexts/userContext";

import "./recipeSuggestion.scss";

interface Recipe {
  title: string;
  ingredients: string[];
  instructions: string[];
}

interface RecipeResponse {
  recipes: Recipe[];
}

const fetchRecipe = async (userId: string): Promise<RecipeResponse> => {
  const response = await fetch(`/api/get_suggested_recipe?fridge_id=${userId}`);

  if (!response.ok) {
    throw new Error("Failed to fetch recipe");
  }

  return await response.json();
};

export const RecipeSuggestion = () => {
  const { user } = useAuth();
  const userId = "0NNRFLhbXJRFk3ER2_iTr8VulFm4";

  const { data, isLoading, error } = useQuery<RecipeResponse, Error>({
    queryKey: ["recipeSuggestion", userId],
    queryFn: () => fetchRecipe(userId),
  });

  if (isLoading) return <Loader />;
  if (error) return <p className="error-message">Error: {error.message}</p>;

  const recipes = data?.recipes ?? [];
  
  if (recipes.length === 0) return <p className="no-recipe">No recipe for today</p>;

  return (
    <motion.div
      className="recipe-container"
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <h3 className="recipe-title">Suggested Recipes</h3>
      {recipes.map((recipe, index) => (
        <div key={index} className="recipe-card">
          <h4 className="recipe-title">{recipe.title}</h4>
          
          <h5>Ingredients:</h5>
          <div className="ingredient-list">
            {recipe.ingredients.map((ingredient, i) => (
              <p key={i} className="ingredient-item">{ingredient.replace(/^- /, "")}</p> // Removes leading dash
            ))}
          </div>

          <h5>Instructions:</h5>
          <div className="instruction-list">
            {recipe.instructions.map((instruction, i) => (
              <p key={i} className="instruction-item">{instruction.replace(/^\d+\.\s/, "")}</p> // Removes leading numbers
            ))}
          </div>
        </div>
      ))}
    </motion.div>
  );
};
