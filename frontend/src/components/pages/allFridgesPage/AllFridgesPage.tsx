import { Options } from "./options";

interface Fridge {
  fridge_id: string;
  fridge_name: string;
}

const fetchFridges = async (): Promise<Fridge[]> => {
  const response = await fetch("/api/get_all_fridges?user_id=0NNRFLhbXJRFk3ER2_iTr8VulFm4");
  if (!response.ok) throw new Error("Failed to fetch data");
  return response.json();
};

export const AllFridgesPage = () => {
  return (
    <Options
      title="YOUR FRIDGES"
      subtitle="What fridge do you want to check?"
      queryKey={["fridges"]}
      queryFn={fetchFridges}
      filterFn={(fridge, query) => fridge.fridge_name.toLowerCase().includes(query)}
      itemKey={(fridge) => fridge.fridge_id}
      itemLabel={(fridge) => fridge.fridge_name}
      itemLink={(fridge) => `${fridge.fridge_id}`}
    />
  );
};
