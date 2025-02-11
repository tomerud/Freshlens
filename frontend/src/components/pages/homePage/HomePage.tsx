import { GraphSection } from './graphSection';

import './homePage.scss';

export const HomePage = () => {

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
        <div className="p-4 border-b shadow-md bg-white">
          <h1 className="text-2xl font-bold freshlens-title">FRESHLENS</h1>
          <p className="text-gray-500">{formattedDate}</p>
        </div>
      </header>

      <div className='notifications'>
        <button className='notification-btn'>2 New Notifications</button>
        <button className='see-all-btn'>See all</button>
        <div className='alert-message'>
          The cucumbers in your fridge expire soon.
        </div>
      </div>

      <GraphSection />
    </>
  );
};
