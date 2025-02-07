import { useNavigate } from "react-router-dom";
import classNames from "classnames"; 

import './FridgeHeader.scss'

interface ProductPageProps {
  title: string;
  subtitle: string;
  showBackButton?: boolean;
}

export const FridgeHeader = ({ title, subtitle, showBackButton = true } :ProductPageProps) => {
  const navigate = useNavigate();

  return (
    <>
      <header className="header">
      <button hidden={!showBackButton} className="back-button" onClick={() => navigate(-1)}>←</button>
        <h1 className={classNames({ BackButtonHidden: !showBackButton })}>{title}</h1>
        <button className="search-button">🔍</button>
      </header>
      <p className="fridge-subtext">{subtitle}</p>
    </>
  );
};