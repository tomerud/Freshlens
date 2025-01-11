
import './App.css'
import { Footer } from './components/footer';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import { HomePage } from './components/pages/homePage';
import { FridgePage } from './components/pages/fridgePage';
import { UserProfilePage } from './components/pages/userProfilePage';
import { Shelf } from './components/pages/fridgePage/shelf';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/basket" element={<UserProfilePage />} />
        <Route path="/fridge" element={<FridgePage />} />
        <Route path="/fridge/shelf/:shelfName" element={<Shelf />} />
        <Route path="/user/*" element={<UserProfilePage />} />
      </Routes>
      <Footer />
    </Router>
  );
}

export default App
