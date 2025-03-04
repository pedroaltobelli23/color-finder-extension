import { useRef, useEffect, useState } from "react";

const colors = {'olive': ["176", "170",  "65"], 'silver': ["190", "198", "205"], 'darkblue': [ "33", "102", "202"], 'gray': ["90", "78", "47"]}

export default function ColorFinder() {
  const canvasRef = useRef(null);
  const [hoveredColor, setHoveredColor] = useState(null);
  const imageSrc = "/result.png"; // Altere para o caminho correto

  useEffect(() => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext("2d");
    const img = new Image();
    img.src = imageSrc;
    img.onload = () => {
      console.log(img.width)
      canvas.width = img.width;
      canvas.height = img.height;
      ctx.drawImage(img, 0, 0);
    };
  }, [imageSrc]);

  const checkPixel = (pixel) => {
    let closestColor = null;
    let smallestDiff = Infinity;

    for (const [colorName, colorRGB] of Object.entries(colors)) {
        const diff = Math.abs(pixel[0] - colorRGB[0]) +
                     Math.abs(pixel[1] - colorRGB[1]) +
                     Math.abs(pixel[2] - colorRGB[2]);

        if (diff < smallestDiff) {
            smallestDiff = diff;
            closestColor = colorName;
        }
    }
    console.log(closestColor)
    return closestColor;
  };

  const handleMouseMove = (e) => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext("2d", { willReadFrequently: true });
    const rect = canvas.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    const pixel = ctx.getImageData(x, y, 1, 1).data;
    const closestColor = checkPixel(pixel)
    const colorhex = `#${pixel[0].toString(16).padStart(2, "0")}${pixel[1].toString(16).padStart(2, "0")}${pixel[2].toString(16).padStart(2, "0")}`;
    setHoveredColor({ name: closestColor, color: colorhex });
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
