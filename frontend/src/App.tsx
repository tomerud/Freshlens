
import './App.css'
import { Footer } from './components/footer';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import { HomePage } from './components/pages/homePage';
import { FridgePage } from './components/pages/fridgePage';
import { UserProfilePage } from './components/pages/userProfilePage';
import { CategoryPage } from './components/pages/fridgePage/category';
import { CamerasPage } from './components/pages/camerasPage';
import { ProductPage } from './components/pages/fridgePage/category/productPage';
import { AllFridgesPage } from './components/pages/allFridgesPage';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/basket" element={<UserProfilePage />} />
        <Route path="/fridges" element={<AllFridgesPage />} />
        <Route path="/fridges/:fridgeId" element={<FridgePage />} />
        <Route path="/fridges/:fridgeId/:categoryName" element={<CategoryPage />} />
        <Route path="/fridges/:fridgeId/:categoryName/:productId" element={<ProductPage />} />
        <Route path="/cameras" element={<CamerasPage />} />
        <Route path="/user/*" element={<UserProfilePage />} />
      </Routes>
      <Footer />
    </Router>
  );
}

export default App
