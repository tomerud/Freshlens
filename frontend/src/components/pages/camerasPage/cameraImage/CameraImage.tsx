import _ from "lodash";
import { FridgeImages } from "../CamerasPage";
import "./cameraImage.scss";

export const CameraImage = ({ fridge_name, images }: FridgeImages) => {
  return (
    <>
      <h2 className="fridge-name">{_.startCase(_.toLower(fridge_name))}</h2>
      <div className="camera-images">
        {images.map((image, index) => (
          <div key={index} className="image-card">
            <img src={image.image_base64}
                 alt={image.camera_ip}
                 className="fetched-image"
            />
            <p className="camera-timestamp">{new Date(image.timestamp).toLocaleString()}</p>
          </div>
        ))}
      </div>
      </>
  );
};
