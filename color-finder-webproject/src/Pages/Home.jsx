import { useState, useEffect } from "react";

export default  function Home() {
    const [image, setImage] = useState(null);

	window.addEventListener("imagemmm", ({data}) => {
		window.postMessage("received","*");
		console.log("ATUMALAKA")
		console.log(data)
	});

    return (
        <div>
            {image ? <img src={image} alt="Received" /> : <p>No image received</p>}
        </div>
    );
}