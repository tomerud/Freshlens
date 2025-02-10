import { useMutation } from "@tanstack/react-query";
import axios from "axios";
import "./camerasPage.scss";

interface ImageResponse {
  user_id: string;
  camera_ip: string;
  image_base64: string;
  timestamp: string;
}

const fetchImage = async (): Promise<ImageResponse> => {
  // GET request to the Flask endpoint (no body, since it’s hardcoded in Flask)
  const response = await axios.get("/api/get_picture");

  if (!response.data.image_base64) {
    throw new Error("No image found");
  }
  return response.data;
};

export const CamerasPage = () => {
  const { mutate, data, isPending, error } = useMutation<ImageResponse, Error>({
    mutationFn: fetchImage
  });

  return (
    <div className="image-fetcher-container">
      <h2 className="title">Fetch Image for user123</h2>
      <button onClick={() => mutate()}>Get Image</button>

      {isPending && <div>Loading...</div>}
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
