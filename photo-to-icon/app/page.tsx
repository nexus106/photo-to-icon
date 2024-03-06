"use client";

import { ChakraProvider } from "@chakra-ui/react";
import ImageUploader from "@/components/ImageUploder";

const Home = () => {
	return (
		<ChakraProvider>
			<ImageUploader />
		</ChakraProvider>
	);
};

export default Home;
