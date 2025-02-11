import { useState } from "react";
import { useNavigate } from "react-router-dom";
import classNames from "classnames"; 

import './FridgeHeader.scss';

interface ProductPageProps {
  title: string;
  subtitle: string;
  showBackButton?: boolean;
  onSearch?: (query: string) => void;
}

export const FridgeHeader = ({ title, subtitle, showBackButton = true, onSearch }: ProductPageProps) => {
  const navigate = useNavigate();
  const [showSearch, setShowSearch] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");

  const toggleSearch = () => {
    if (showSearch) {
      setSearchQuery("");
      onSearch?.("");
    }
    setShowSearch(!showSearch);
  };

  const handleSearchChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setSearchQuery(value);
    onSearch?.(value);
  };

  return (
    <>
      <header className="fridge-header">
        <button className={classNames("back-button", { hidden: !showBackButton })} onClick={() => navigate(-1)}>←</button>

        {showSearch ? (
          <input 
            type="text"
            className="search-input"
            placeholder="Search..."
            value={searchQuery}
            onChange={handleSearchChange}
            autoFocus
          />
        ) : (
          <h1>{title}</h1>
        )}

        <button className={classNames("search-button", { hidden: !onSearch })} onClick={toggleSearch}>
          {showSearch ? (
            <img src="/icons/cancel-icon.png" alt="Cancel" className="cancel-icon" />
          ) : (
            <img src="/icons/search-icon.png" alt="Search" className="search-icon" />
          )}
        </button>
      </header>
      <p className="fridge-subtext">{subtitle}</p>
    </>
  );
};
