import { useState, useEffect } from "react";

export function useSearch<T>(data: T[], filterFunction: (item: T, query: string) => boolean) {
    const [searchQuery, setSearchQuery] = useState<string>("");
    const [filteredResults, setFilteredResults] = useState<T[]>(data);

    useEffect(() => {
        if (!searchQuery) {
            setFilteredResults(data);
        } else {
            setFilteredResults(data.filter(item => filterFunction(item, searchQuery.toLowerCase())));
        }
    }, [searchQuery, data]);

    return { filteredResults, searchQuery, setSearchQuery };
}