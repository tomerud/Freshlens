import './graphSection.scss';

export const GraphSection = () => {
  return (
    <>
      <div className='fridge-info'>
        <div className='fridge-freshness'>
          <h2>82%</h2>
          <p>FRIDGE FRESHNESS</p>
        </div>
        <div className='smart-buy'>
          <h2>SMART BUY</h2>
        </div>
      </div>

      <div className='graph-section'>
        <div className='time-selectors'>
          <button>1W</button>
          <button className='active'>1M</button>
          <button>1Y</button>
        </div>
        <div className='graph'>
          <p>Graph Placeholder</p>
        </div>
      </div>
    </>
  );
};
