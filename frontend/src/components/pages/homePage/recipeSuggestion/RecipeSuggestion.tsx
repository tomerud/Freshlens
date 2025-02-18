import { useQuery } from "@tanstack/react-query";
import { useParams } from "react-router-dom";
import { useMemo } from "react";
import { Loader } from "../../../loader";
import { FridgeHeader } from "../../allFridgesPage/fridgeHeader";

import "./recipeSuggestion.scss";

interface Recipe {
  title: string;
  ingredients: string[];
  instructions: string[];
}

interface RecipeResponse {
  recipes: Recipe[];
}

const fetchRecipe = async (fridgeId: string): Promise<RecipeResponse> => {
  const response = await fetch(`/api/get_suggested_recipe?fridge_id=${fridgeId}`);

  if (!response.ok) {
    throw new Error("Failed to fetch recipe");
  }

  return await response.json();
};

export const RecipeSuggestion = () => {
  const { fridgeId } = useParams<{ fridgeId?: string }>();

  const { data, isLoading, error } = useQuery<RecipeResponse, Error>({
    queryKey: fridgeId ? ["recipeSuggestion", fridgeId] : ["recipeSuggestion"],
    queryFn: () => fetchRecipe(fridgeId as string),
    enabled: !!fridgeId,
  });

  const recipes = useMemo(() => data?.recipes ?? [], [data]);

  return (
    <>
      <FridgeHeader title="Recipes" subtitle="Recipes to use still good products!" />
  
      {!fridgeId && <p className="error-message">Invalid fridge ID</p>}
  
      <div className="recipe-container">
        {isLoading && <Loader />}
        {error && <p className="error-message">Error: {error.message}</p>}
        {!isLoading && !error && recipes.length === 0 && (
          <h4 className="no-recipe">No recipe for today</h4>
        )}
        {!isLoading && !error && recipes.length > 0 &&
          recipes.map((recipe, index) => (
            <div key={index} className="recipe-card">
              <p className="recipe-title">{recipe.title}</p>
              <p className="section-header">Ingredients:</p>
              <ul className="ingredient-list">
                {recipe.ingredients.map((ingredient, i) => (
                  <li key={i} className="ingredient-item">• {ingredient.replace(/^- /, "")}</li>
                ))}
              </ul>
              <p className="section-header">Instructions:</p>
              <ol className="instruction-list">
                {recipe.instructions.map((instruction, i) => (
                  <li key={i} className="instruction-item">{i + 1}. {instruction.replace(/^\d+\.\s/, "")}</li>
                ))}
              </ol>
            </div>
          ))
        }
      </div>
    </>
  );
};
