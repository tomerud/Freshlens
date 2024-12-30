import { useQuery } from '@tanstack/react-query';

import './homePage.scss'

interface ApiData {
    Name: string;
    Age: number;
    Date: string;
  }
  
  const fetchData = async (): Promise<ApiData> => {
    const response = await fetch('/api/data');
    if (!response.ok) {
      throw new Error('Failed to fetch data');
    }
    return response.json();
  };

  export const HomePage = () => {
    const { data, isLoading, error } = useQuery<ApiData, Error>({
      queryKey: ['apiData'],
      queryFn: fetchData,
    });
  
    if (isLoading) return <p>Loading...</p>;
    if (error instanceof Error) return <p>Error: {error.message}</p>;
  
    return (
        <>
        <div>
        <a href="./public/FreshLens.png" target="_blank">
          <img src={"./public/FreshLens.png"} className="logo" alt="Vite logo" />
        </a>
        </div>
        <h1>FreshLens</h1>
        <p>{data?.Name}</p>
        <p>{data?.Age}</p>
        <p>{data?.Date}</p>
        </>
    );
  }


