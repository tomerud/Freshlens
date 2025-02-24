import { MoneySaveGraph } from './moneySaveGraph';
import { ShoppingCartLink } from './shoppingCartLink';
import { FridgeFreshness } from './fridgeFrehsness';

import './graphSection.scss';

export const GraphSection = () => {
  
  return (
    <>
      <div className="cards-container">
        <ShoppingCartLink/>
        <FridgeFreshness/>
      </div>
      <MoneySaveGraph />
    </>
  );
};
