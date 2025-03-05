import { useRef, useEffect, useState } from "react";

const colors = {'darkgoldenrod': [204, 194,  66], 'saddlebrown': [117,  99,  49], 'lightcyan': [200, 213, 238], 'cadetblue': [ 15,  59, 149], 'darkmagenta': [160, 159,  52], 'black': [26, 25, 34], 'aquamarine': [ 51, 131, 233], 'silver': [187, 191, 178], 'tan': [170, 159, 122]}

export default function ColorFinder() {
  const canvasRef = useRef(null);
  const [hoveredColor, setHoveredColor] = useState(null);
  const imageSrc = "/result.png"; // Base image
  const overlaySrc = "/resized.png"; // Image to overlay

  useEffect(() => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext("2d");
    const img = new Image();
    img.src = imageSrc;

    img.onload = () => {
      canvas.width = img.width;
      canvas.height = img.height;
      ctx.drawImage(img, 0, 0);

      // Load and draw overlay image
      const overlay = new Image();
      overlay.src = overlaySrc;
      overlay.onload = () => {
        ctx.drawImage(overlay, 0, 0);
      };
    };
  }, [imageSrc, overlaySrc]);

  const checkPixel = (pixel) => {
    let closestColor = null;
    let smallestDiff = Infinity;

    for (const [colorName, colorRGB] of Object.entries(colors)) {
      const diff =
        Math.abs(pixel[0] - colorRGB[0]) +
        Math.abs(pixel[1] - colorRGB[1]) +
        Math.abs(pixel[2] - colorRGB[2]);

      if (diff < smallestDiff) {
        smallestDiff = diff;
        closestColor = colorName;
      }
    }
    return closestColor;
  };

  const handleMouseMove = (e) => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext("2d", { willReadFrequently: true });
    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;

    // Get the pixel color from the base image
    const pixel = ctx.getImageData(x, y, 1, 1).data;
    const closestColor = checkPixel(pixel);
    const closestColorRGB = colors[closestColor]
    const colorHex = `#${parseInt(closestColorRGB[0], 10).toString(16).padStart(2, "0")}${parseInt(closestColorRGB[1], 10)
      .toString(16)
      .padStart(2, "0")}${parseInt(closestColorRGB[2], 10).toString(16).padStart(2, "0")}`;
    console.log(colorHex)
    setHoveredColor({ name: closestColor, color: colorHex });
  };

  return (
    <div style={{ position: "relative" }}>
      <canvas ref={canvasRef} onMouseMove={handleMouseMove} />
      {hoveredColor && (
        <div
          style={{
            position: "absolute",
            top: 10,
            left: 10,
            background: hoveredColor.color,
            padding: "5px 10px",
            borderRadius: "5px",
            boxShadow: "0px 0px 5px rgba(0,0,0,0.3)",
          }}
        >
          {hoveredColor.name}
        </div>
      )}
    </div>
  );
}
