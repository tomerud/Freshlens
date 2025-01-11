import { useQuery } from '@tanstack/react-query';

import './homePage.scss';
import { GraphSection } from './graphSection';

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

  const today = new Date();
  const options: Intl.DateTimeFormatOptions = {
    weekday: 'long',
    day: 'numeric',
    month: 'long',
    year: 'numeric',
  };
  const formattedDate = today.toLocaleDateString('en-US', options);

  return (
    <>
      <header className='header'>
        <h1>FreshLens</h1>
        <p>{formattedDate}</p>
        <a href='./public/FreshLens.png' target='_blank'>
          <img
            src={'./public/FreshLens.png'}
            className='logo'
            alt='Vite logo'
          />
        </a>
      </header>

      <div className='notifications'>
        <button className='notification-btn'>2 New Notifications</button>
        <button className='see-all-btn'>See all</button>
        <div className='alert-message'>
          The cucumbers in your fridge expire soon.
        </div>
      </div>

      <GraphSection />

      {/* <p>{data?.Name}</p>
      <p>{data?.Age}</p>
      <p>{data?.Date}</p> */}
    </>
  );
};
