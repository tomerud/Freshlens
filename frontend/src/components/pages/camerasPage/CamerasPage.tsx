import { useQuery } from '@tanstack/react-query';

import './camerasPage.scss';

// interface ApiData {
//   Name: string;
//   Age: number;
//   Date: string;
// }

// const fetchData = async (): Promise<ApiData> => {
//   const response = await fetch('/api/data');
//   if (!response.ok) {
//     throw new Error('Failed to fetch data');
//   }
//   return response.json();
// };

export const CamerasPage = () => {
  // const { data, isLoading, error } = useQuery<ApiData, Error>({
  //   queryKey: ['apiData'],
  //   queryFn: fetchData,
  // });

  // if (isLoading) return <p>Loading...</p>;
  // if (error instanceof Error) return <p>Error: {error.message}</p>;

  return (
    <>
      <span>cameras will be here</span>
    </>
  );
};
