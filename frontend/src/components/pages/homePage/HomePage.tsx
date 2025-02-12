
import { HomePageHeader } from './homePageHeader';
import { Notifications } from './notifications';
import { GraphSection } from './graphSection';
import { TipsSection } from '../../TipsSection';
import { RecipeSuggestion } from './recipeSuggestion';

import 'react-circular-progressbar/dist/styles.css';
import './homePage.scss';


export const HomePage = () => {

  return (
    <>
      <HomePageHeader />
      <div className='homepage-container'>
        <Notifications />
        <GraphSection />
        <TipsSection />
        <RecipeSuggestion />
      </div>
    </>
  );
};
