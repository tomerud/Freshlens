import { Link } from 'react-router-dom';
import './fridgePage.scss';

export const FridgePage = () => {
  const shelves = ['VEGETABLES', 'FRUIT', 'DAIRY', 'SAUCES', 'FISH & MEAT'];

  return (
    <>
      <h1>FridgePage</h1>
      <div className='fridge-container'>
        <button className='search-button'>🔍</button>
        <div className='shelves-list'>
          {shelves.map((shelf, index) => (
            <Link
              key={index}
              to={`shelf/${shelf.toLowerCase()}`}
              className='shelf-item'
            >
              {shelf}
            </Link>
          ))}
        </div>
      </div>
    </>
  );
};
