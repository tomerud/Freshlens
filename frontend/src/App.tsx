
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import { HomePage } from './components/pages/homePage';
import { UserProfilePage } from './components/pages/userProfilePage';
import { CamerasPage } from './components/pages/camerasPage';
import { AllFridgesPage } from './components/pages/allFridgesPage';
import { AuthProvider } from './contexts/userContext';
import { PrivateRoute } from './components/PrivateRoute';
import { LoginPage } from './components/pages/userProfilePage/LoginPage/LoginPage';
import { Layout } from './components/Layout';
import { FridgePage } from './components/pages/allFridgesPage/fridgePage';
import { CategoryPage } from './components/pages/allFridgesPage/fridgePage/category';
import { ProductPage } from './components/pages/allFridgesPage/fridgePage/category/productPage';

import './App.css'
import { RecipeSuggestion } from './components/pages/homePage/recipeSuggestion';
import { ShoppingCart } from './components/pages/homePage/shoppingCart';

function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          
          <Route element={<PrivateRoute><Layout /></PrivateRoute>}>
            <Route path="/" element={<HomePage />} />
            <Route path="/fridges" element={<AllFridgesPage />} />
            <Route path="/fridges/:fridgeId" element={<FridgePage />} />
            <Route path="/fridges/recipes/:fridgeId" element={<RecipeSuggestion />} />
            <Route path="/fridges/:fridgeId/:categoryName" element={<CategoryPage />} />
            <Route path="/fridges/:fridgeId/:categoryName/:productId" element={<ProductPage />} />
            <Route path="/cameras" element={<CamerasPage />} />
            <Route path="/user/*" element={<UserProfilePage />} />
            <Route path="/ShoppingCart/" element={<ShoppingCart />} />
          </Route>
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App
