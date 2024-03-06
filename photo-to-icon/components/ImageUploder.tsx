import React, { useState } from "react";
import { Box, Button, Image } from "@chakra-ui/react";

function ImageUploader() {
	const [selectedImage, setSelectedImage] = useState(null);
	const [imageUrl, setImageUrl] = useState("");

	// 画像をAPIに送信し、結果を処理する関数
	const handleSubmit = async () => {
		if (!selectedImage) return;

		const formData = new FormData();
		formData.append("upload_file", selectedImage);

		try {
			const response = await fetch("http://127.0.0.1:9004/upload", {
				method: "POST",
				body: formData,
			});

			if (!response.ok) throw new Error("Something went wrong");

			const data = await response.json();
			setImageUrl(data.image_url); // JSONの`image_url`を取得してstateにセット
		} catch (error) {
			console.error(error);
		}
	};

	return (
		<Box>
			<input
				type="file"
				accept=".jpg, .jpeg, .png"
				onChange={(e) => setSelectedImage(e.target.files[0])}
			/>
			<Button onClick={handleSubmit}>Upload</Button>
			{imageUrl && (
				<Image src={imageUrl} boxSize="400px" alt="generated image" />
			)}
		</Box>
	);
}

export default ImageUploader;
