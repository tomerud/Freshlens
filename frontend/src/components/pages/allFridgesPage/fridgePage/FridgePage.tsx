import _ from 'lodash';
import {Link, useParams } from 'react-router-dom';
import { Options } from '../options';

import './FridgePage.scss';

interface Category {
    categoryId: number;
    categoryName: string;
  }
  
  const fetchCategories = async (fridgeId: string): Promise<Category[]> => {
    const response = await fetch(`/api/get_all_categories?fridge_id=${fridgeId}`);
    if (!response.ok) throw new Error("Failed to fetch categories");
    return response.json();
  };
  
  export const FridgePage = () => {
    const { fridgeId } = useParams<{ fridgeId?: string }>();

    if (!fridgeId) return <p className="error-message">Invalid fridge ID</p>;
  
    return (
      <>
        <Options
        title="My Fridge"
        subtitle="Choose a category"
        queryKey={["categories", fridgeId]}
        queryFn={() => fetchCategories(fridgeId!)}
        filterFn={(category, query) => category.categoryName.toLowerCase().includes(query)}
        itemKey={(category) => category.categoryId}
        itemLabel={(category) => category.categoryName}
        itemLink={(category) => `${category.categoryName}`}
        />
        <button className="recipe-button">
          <Link key={fridgeId} to={`/fridges/recipes/${fridgeId}`}>
            Get Recipe!
          </Link>
        </button>
      </>
    );
  };