import { Bar, BarChart, ResponsiveContainer, Tooltip, XAxis, YAxis, Cell } from 'recharts';

import './moneySaveGraph.scss';

const data = [
  { month: "Jan", value: 125 },
  { month: "Feb", value: 100 },
  { month: "Mar", value: 60 },
  { month: "Apr", value: 90 },
  { month: "May", value: 30 },
  { month: "Jun", value: 150 },
  { month: "Jul", value: 80 },
  { month: "Aug", value: 60 },
  { month: "Sep", value: 130 },
  { month: "Oct", value: 100 }
];

const getBarColor = (value: number) => {
  if (value > 100) return "#000";
  if (value >= 50) return "#2C5E74";
  return "#D66B4A";
};

export const MoneySaveGraph = () => {
  return (
    <div className="graph-section">
      <p className="card-label">Saving Money</p>
      <div className="graph-container">
        <ResponsiveContainer width="100%" height={150}>
          <BarChart data={data} barSize={20}>
            <XAxis dataKey="month" axisLine={false} tickLine={false} />
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
