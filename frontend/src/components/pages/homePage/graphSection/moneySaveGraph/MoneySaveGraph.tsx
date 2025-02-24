import { Bar, BarChart, ResponsiveContainer, Tooltip, XAxis, YAxis, Cell } from 'recharts';
import { Loader } from '../../../../loader';
import { useQuery } from '@tanstack/react-query';

import './moneySaveGraph.scss';

interface MoneySaveData {
  week: string;
  value: number;
}

const fetchMoneySaveData = async (userId: string): Promise<MoneySaveData[]> => {
  const response = await fetch(`/api/get_money_save_data?user_id=${userId}`);
  if (!response.ok) throw new Error("Failed to fetch money saving data");
  return response.json();
};

const getBarColor = (value: number) => {
  if (value > 100) return "#000";
  if (value >= 50) return "#2C5E74";
  return "#D66B4A";
};

export const MoneySaveGraph = () => {
  const userId = "0NNRFLhbXJRFk3ER2_iTr8VulFm4";

  const { data, isLoading, error } = useQuery<MoneySaveData[], Error>({
    queryKey: userId ? ["MoneySaveData", userId] : ["MoneySaveData"],
    queryFn: () => fetchMoneySaveData(userId),
    enabled: !!userId,
  });

  if (isLoading) return <Loader />;
  if (error) return <div>Error: {error.message}</div>;
  if (!data) return <div>No data available</div>;
  
  return (
    <div className="graph-section">
      <p className="card-label">Saving Money</p>
      <div className="graph-container">
        <ResponsiveContainer width="100%" height={150}>
          <BarChart data={data} barSize={20}>
            <XAxis dataKey="week" axisLine={false} tickLine={false} />
            <YAxis hide />
            <Tooltip />
            <Bar dataKey="value" radius={[4, 4, 0, 0]}>
              {data.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={getBarColor(entry.value)} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};
