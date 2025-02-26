import { useQuery } from "@tanstack/react-query";

import { useAuth } from "../../../contexts/userContext";
import { Loader } from "../../loader";
import { FridgeHeader } from "../allFridgesPage/fridgeHeader";
import { CameraImage } from "./cameraImage";

import "./camerasPage.scss";

interface CameraImage {
  camera_ip: string;
  image_base64: string;
  timestamp: string;
}

export interface FridgeImages {
  fridge_id: number;
  fridge_name: string;
  images: CameraImage[];
}

interface CameraImagesResponse {
  user_id: string;
  fridges: FridgeImages[];
}

const fetchImages = async (userId: string | undefined): Promise<CameraImagesResponse> => {
  const response = await fetch(`/api/get_image?user_id=${userId}`);
  if (!response.ok) throw new Error("Failed to fetch images");
  return response.json();
};

export const CamerasPage = () => {
  const { user } = useAuth();

  const { data, isLoading, error, refetch } = useQuery({
    queryKey: ["cameraImages", user?.uid],
    queryFn: () => fetchImages(user?.uid),
    enabled: !!user?.uid,
    refetchOnWindowFocus: false,
  });

  const fridges = data?.fridges ?? [];

  return (
    <>
      <FridgeHeader title="REAL TIME VIEW" subtitle="Watch your fridge from everywhere" showBackButton={false} />
      {isLoading && <Loader />}
      {error && <div className="error">Error: {error.message}</div>}
      {fridges.length > 0 ? (
        <div className="image-grid">
          {fridges.map((fridge) => (
            <CameraImage key={fridge.fridge_id} {...fridge} />
          ))}
        </div>
      ) : (
        <p className="no-images">No images available.</p>
      )}
      <button className="refresh-button" onClick={() => refetch()}>Refresh Images</button>
    </>
  );
};
