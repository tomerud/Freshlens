import { Link } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';

import './allFridgesPage.scss';
import { FridgeHeader } from '../fridgePage/fridgeHeader';

interface Fridge {
    fridge_id : string;
    fridge_name: string;
  }
  
  const fetchData = async (userId: string): Promise<Fridge[]> => {
    const response = await fetch(`/api/get_all_fridges?user_id=${userId}`);
  
    if (!response.ok) {
      throw new Error('Failed to fetch data');
    }
    return await response.json();
  };

export const AllFridgesPage = () => {
    const userId = '0NNRFLhbXJRFk3ER2_iTr8VulFm4';
    const { data: fridges = [], isLoading, error } = useQuery<Fridge[], Error>({
      queryKey: ['categories', userId],
      queryFn: () => fetchData(userId),
    });
  
    if (isLoading) return <p>Loading...</p>;
    if (error) return <p>Error: {error.message}</p>;
    
    return (
        <div className="fridge-page">
          <FridgeHeader title={'YOUR FRIDGES'} subtitle="what fridge you want to check?" showBackButton={false} />
          <div className="category-list">
              {fridges?.map((fridge) => (
              <Link key={fridge.fridge_id} to={`${fridge.fridge_id}`} className="category-item">
                  {fridge.fridge_name}
              </Link>
              ))}
          </div>
        </div>
    );
};