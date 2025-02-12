import { Link, useParams } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { useSearch } from '../allFridgesPage/hooks/useSearch';
import { FridgeHeader } from './fridgeHeader';
import { Loader } from '../../loader';

import './FridgePage.scss';

interface Category {
    category_id: number;
    category_name: string;
}

interface Fridge {
    fridge_id: string;
    fridge_name: string;
}

const fetchCategories = async (fridgeId: string): Promise<Category[]> => {
    const response = await fetch(`/api/get_all_categories?fridge_id=${fridgeId}`);
    if (!response.ok) throw new Error('Failed to fetch categories');
    return await response.json();
};

const fetchFridgeName = async (fridgeId: string): Promise<Fridge> => {
    const response = await fetch(`/api/get_fridge_name?fridge_id=${fridgeId}`);
    if (!response.ok) throw new Error('Failed to fetch fridge name');
    return await response.json();
};

export const FridgePage = () => {
    const { fridgeId } = useParams<{ fridgeId: string }>();

    const { data: fridge, isLoading: loadingFridge, error: fridgeError } = useQuery<Fridge, Error>({
        queryKey: ['fridgeName', fridgeId],
        queryFn: () => fetchFridgeName(fridgeId!),
    });

    const { data: categories = [], isLoading: loadingCategories, error: categoryError } = useQuery<Category[], Error>({
        queryKey: ['categories', fridgeId],
        queryFn: () => fetchCategories(fridgeId!),
    });

    const { filteredResults, setSearchQuery } = useSearch(categories, 
        (category, query) => category.category_name.toLowerCase().includes(query)
    );

    if (loadingCategories || loadingFridge) return <Loader />;
    if (categoryError) return <p>Error loading categories: {categoryError.message}</p>;
    if (fridgeError) return <p>Error loading fridge name: {fridgeError.message}</p>;

    return (
        <>
            <FridgeHeader
                title={loadingFridge ? "" : fridge?.fridge_name.toUpperCase() || "MY FRIDGE"}
                subtitle="Choose a category"
                onSearch={setSearchQuery} 
            />
            <div className="category-list">
                {filteredResults.length > 0 ? (
                    filteredResults.map((category) => (
                        <Link key={category.category_id} to={`${category.category_name}`} className="category-item">
                            {category.category_name}
                        </Link>
                    ))
                ) : (
                    <p>No matching categories found.</p>
                )}
            </div>
        </>
    );
};
