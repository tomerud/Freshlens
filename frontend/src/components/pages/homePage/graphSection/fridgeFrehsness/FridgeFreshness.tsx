
import { useEffect, useState } from 'react';

import { buildStyles, CircularProgressbar } from 'react-circular-progressbar';
import { useQuery } from '@tanstack/react-query';
import { useAuth } from '../../../../../contexts/userContext';

import './fridgeFreshness.scss';

interface FrifgeFreshness {
  avg_freshness_score: number;
}

const fetchFrifgeFreshness = async (userId: string): Promise<FrifgeFreshness> => {
  const response = await fetch(`/api/get_freshness_score?user_id=${userId}`);  
  if (!response.ok) throw new Error("Failed to fetch frifge freshness");

  return response.json();
};

export const FridgeFreshness = () => {
  const [fridgeFreshness, setFridgeFreshness] = useState(0);
  
  const { user } = useAuth();
  if (!user){
    return <div className="error">Error: no userId</div>
  }

  const { data, error } = useQuery<FrifgeFreshness, Error>({
    queryKey: user.uid ? ["FreshnessScore", user.uid] : ["FreshnessScore"],
    queryFn: () => fetchFrifgeFreshness(user.uid),
    enabled: !!user.uid,
  });

  if (error) return <div>Error: {error.message}</div>;

  useEffect(() => {
    if (!data) return;
    const fridgeFreshnessTimeout = setTimeout(
      () => setFridgeFreshness(data.avg_freshness_score),
      300
    );
    return () => clearTimeout(fridgeFreshnessTimeout);
  }, [data]);


  return (
        <div>
          <p className="card-label">Fridge Freshness</p>
          <div className="card">
            <CircularProgressbar 
              value={fridgeFreshness} 
              text={`${fridgeFreshness}%`} 
              styles={buildStyles({
                textSize: '20px',
                pathColor: '#66bb6a',
                textColor: '#000',
                trailColor: '#eee',
              })}
            />
          </div>
        </div>
  );
};
