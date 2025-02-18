import _ from "lodash";
import { Link } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import { Loader } from "../../../loader";
import { useSearch } from "../hooks/useSearch";
import { FridgeHeader } from "../fridgeHeader";

import './options.scss'

interface OptionsProps<T> {
  title: string;
  subtitle: string;
  queryKey: unknown[];
  queryFn: () => Promise<T[]>;
  filterFn: (item: T, query: string) => boolean;
  itemKey: (item: T) => string | number;
  itemLabel: (item: T) => string;
  itemLink: (item: T) => string;
}

export const Options = <T,>({
  title,
  subtitle,
  queryKey,
  queryFn,
  filterFn,
  itemKey,
  itemLabel,
  itemLink,
}: OptionsProps<T>) => {
  const { data: items = [], isLoading, error } = useQuery<T[], Error>({
    queryKey,
    queryFn,
  });

  const { filteredResults, setSearchQuery } = useSearch(items, filterFn);

  if (isLoading) return <Loader />;
  if (error) return <p>Error: {error.message}</p>;

  return (
    <>
      <FridgeHeader title={title} subtitle={subtitle} onSearch={setSearchQuery} />
      <div className="option-list">
        {filteredResults.length > 0 ? (
          filteredResults.map((item) => (
            <Link key={itemKey(item)} to={itemLink(item)} className="option-item">
              {_.startCase(_.toLower(itemLabel(item)))}
            </Link>
          ))
        ) : (
          <p className="no-options">No matching items found.</p>
        )}
      </div>
    </>
  );
};
