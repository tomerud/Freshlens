import _ from 'lodash';
import {Link, useParams } from 'react-router-dom';
import { Options } from '../options';

import './FridgePage.scss';

interface Category {
    category_id: number;
    category_name: string;
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
        filterFn={(category, query) => category.category_name.toLowerCase().includes(query)}
        itemKey={(category) => category.category_id}
        itemLabel={(category) => category.category_name}
        itemLink={(category) => `${category.category_name}`}
        />
        <button className="recipe-button">
          <Link key={fridgeId} to={`/fridges/recipes/${fridgeId}`}>
            Get Recipe!
          </Link>
        </button>
      </>
    );
  };