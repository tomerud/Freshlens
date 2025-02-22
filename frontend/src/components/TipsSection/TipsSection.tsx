import { useQuery } from "@tanstack/react-query";
import { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import classNames from "classnames"; 

import { Loader } from "../loader";

import "./tipsSection.scss";

interface ProductTips {
  product_name?: string | null;
  refrigerate_tips?: string | null;
  freeze_tips?: string | null;
}

interface TipsSectionProps {
  addedTitle?: string;
  productId?: string;
  classname?: string;
}

const fetchData = async (productId?: string): Promise<ProductTips[]> => {
  const endpoint = productId 
    ? `/api/get_product_tips?product_id=${productId}`
    : `/api/get_general_storage_tips`;

  const response = await fetch(endpoint);
  
  if (!response.ok) {
    throw new Error("Failed to fetch data");
  }

  const data = await response.json();
  return Array.isArray(data) ? data : [];
};

export const TipsSection = ({ addedTitle, productId, classname}: TipsSectionProps) => {
  const { data: tipsData = [], isLoading, error } = useQuery<ProductTips[], Error>({
    queryKey: ["tips", productId],
    queryFn: () => fetchData(productId),
  });

  const tipsArray = tipsData.flatMap((tip) => [
    tip.refrigerate_tips,
    tip.freeze_tips
  ]).filter(Boolean); // Remove null values

  const [currentTipIndex, setCurrentTipIndex] = useState(0);

  useEffect(() => {
    if (tipsArray.length > 1) {
      const interval = setInterval(() => {
        setCurrentTipIndex((prevIndex) => (prevIndex + 1) % tipsArray.length);
      }, 5000);
      return () => clearInterval(interval);
    }
  }, [tipsArray]);

  if (isLoading) return <Loader />;
  if (error) return <div className="tips-error">Error loading tips: {error.message}</div>;
  if (tipsArray.length === 0) return <></>;

  return (
    <div className={classNames("tips-container", classname)}>
      <h3 className="tips-title">{addedTitle} Storage Tip</h3>
      <AnimatePresence mode="wait">
        <motion.p
          key={currentTipIndex}
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -10 }}
          transition={{ duration: 0.5 }}
          className="tips-text"
        >
          {tipsArray[currentTipIndex]}
        </motion.p>
      </AnimatePresence>
    </div>
  );
};
