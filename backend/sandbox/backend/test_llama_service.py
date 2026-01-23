import unittest
from llama_service import load_pipeline, process_image_with_llama

class TestLlamaService(unittest.TestCase):

    def setUp(self):
        """Set up the pipeline for testing."""
        self.pipeline = load_pipeline()

    def test_process_image_with_llama(self):
        """Test the process_image_with_llama function with sample inputs."""
        image_path = "C:\\Users\\Meghan Carr\\Desktop\\Meghan - ALL til OneDrive\\5-0 - Portfolio Projects\\Wetland\\Water prototype\\Wetlands-prototype-MVP\\backend\\sandbox\\images\\AnimalWaterBranches.png"  
        # Replaced with actual image path
        text_prompt = "Describe the image."

        # Call the function
        result = process_image_with_llama(self.pipeline, image_path, text_prompt)

        # Assert the result is not empty
        self.assertIsNotNone(result)
        self.assertIsInstance(result, str)

if __name__ == "__main__":
    unittest.main()