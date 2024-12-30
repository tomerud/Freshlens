import { useState, useEffect } from 'react'
import './App.css'

function App() {
  
  const [data, setdata] = useState({
      name: "",
      age: 0,
      date: "",
  });

  useEffect(() => {
    fetch('/api/data')
      .then((response) => response.json())
      .then((data) => { setdata({ name: data.Name, age: data.Age, date: data.Date})})
      .catch((error) => console.error('Error fetching data:', error));
  }, []);


  return (
    <>
      <div>
        <a href="./public/FreshLens.png" target="_blank">
          <img src={"./public/FreshLens.png"} className="logo" alt="Vite logo" />
        </a>
      </div>
      <h1>FreshLens</h1>
        <p>{data.name}</p>
        <p>{data.age}</p>
        <p>{data.date}</p>               
    </>
  )
}

export default App
