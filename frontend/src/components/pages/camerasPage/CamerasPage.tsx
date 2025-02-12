import { useQuery } from "@tanstack/react-query";
import "./camerasPage.scss";
import { Loader } from "../../loader";

interface ImageResponse {
  user_id: string;
  camera_ip: string;
  image_base64: string;
  timestamp: string;
}

const fetchImage = async (): Promise<ImageResponse> => {
  const response = await fetch("/api/get_image");
  if (!response.ok) throw new Error("Failed to fetch image");
  
  const data = await response.json();
  if (!data.image_base64) throw new Error("No image found");

  return data;
};

export const CamerasPage = () => {
  const { data, isLoading, error, refetch } = useQuery({
    queryKey: ["cameraImage"],
    queryFn: fetchImage,
    enabled: false,
  });

  return (
    <div className="image-fetcher-container">
      <h2 className="title">Fetch Image for user123</h2>
      <button onClick={() => refetch()}>Get Image</button>
      
      {isLoading && <Loader />}
      {error && <div className="error">Error: {error.message}</div>}

      {data && (
        <img
          src={`data:image/jpeg;base64,${data.image_base64}`}
          alt="Fetched"
          className="fetched-image"
        />
      )}
    </div>
  );
};
