import { FridgeImages } from "../CamerasPage";
import "./cameraImage.scss";

export const CameraImage = ({ fridge_name, images }: FridgeImages) => {
  return (
    <>
      <h2 className="fridge-name">{fridge_name}</h2>
      <div className="camera-images">
        {images.map((image, index) => (
          <div key={index} className="image-card">
            <h3 className="camera-ip">{image.camera_ip}</h3>
            <img src={`data:image/jpeg;base64,${image.image_base64}`}
                 alt={image.camera_ip}
                 className="fetched-image"
            />
            <p className="camera-timestamp">Timestamp: {new Date(image.timestamp).toLocaleString()}</p>
          </div>
        ))}
      </div>
      </>
  );
};
