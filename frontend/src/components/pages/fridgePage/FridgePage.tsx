import { Link, useNavigate, useParams } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';

import './fridgePage.scss';
import { FridgeHeader } from './fridgeHeader';

interface Category {
  category_id: number;
  category_name: string;
}

const fetchData = async (fridgeId: number): Promise<Category[]> => {
  const response = await fetch(`/api/get_all_categories?fridge_id=${fridgeId}`);

  if (!response.ok) {
    throw new Error('Failed to fetch data');
  }
  return await response.json();
};

export const FridgePage = () => {
  const navigate = useNavigate();
  const { fridgeId } = useParams<{ fridgeId: string }>();

  const { data: categories = [], isLoading, error } = useQuery<Category[], Error>({
    queryKey: ['categories', fridgeId],
    queryFn: () => fetchData(fridgeId),
  });

  if (isLoading) return <p>Loading...</p>;
  if (error) return <p>Error: {error.message}</p>;

  return (
    <div>
      <FridgeHeader title={'My fridge'} subtitle="All my fridge products"/>
      <div className="category-list">
        {categories?.map((category) => (
          <Link key={category.category_id} to={`${category.category_name}`} className="category-item">
            {category.category_name}
          </Link>
        ))}
      </div>
    </div>
  );
};