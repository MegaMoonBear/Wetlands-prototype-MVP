# This file is responsible for handling communication with the LLaMA Vision AI model.
# The command aligns with the task of setting up the model for use in this module.
# https://huggingface.co/meta-llama/Llama-3.2-11B-Vision-Instruct

# Add command as a comment or part of a setup function...
# ...to ensure the model is downloaded before making API calls.
# The command is used to download the LLaMA Vision model files from Hugging Face. 
# This command is typically part of the setup process for downloading and preparing the model.

# BASH in terminal or command prompt
    # Download the model using the huggingface-cli command.
from xml.etree.ElementInclude import include
from transformers import pipeline


# If not using API for prototype, this file can still be used: 
# Use this file to prepare and test integration with LLaMA Vision model locally

# For Thursday's prototype (no API calls):

            # ONE - Download the model using the huggingface-cli command
            # hf download meta-llama/Llama-3.2-11B-Vision-Instruct --include "original/*" --local-dir Llama-3.2-11B-Vision-Instruct
                    # DEPRECATED: huggingface-cli download meta-llama/Llama-3.2-11B-Vision-Instruct --include "original/*" --local-dir Llama-3.2-11B-Vision-Instruct

# TWO to FOUR addressed by next code block
    # Load the model locally using libraries like Hugging Face's transformers.
    # Process the image and text inputs and pass them to the model.
    # Parse the model's output for further use.
# Use a pipeline as a high-level helper
# llama_service.py
# Handles communication with the LLaMA Vision AI model using Hugging Face's transformers library.

from transformers import pipeline

def load_pipeline():
    """
    Load the LLaMA Vision pipeline.

    Returns:
        pipeline: The loaded Hugging Face pipeline for image-text-to-text tasks.
    """
    try:
        # Load the pipeline using the local model path
        return pipeline("image-text-to-text", model="./path/to/local/model")
    except Exception as e:
        raise RuntimeError(f"Failed to load the pipeline: {e}")
    
def process_image_with_llama(pipe, image_path, text_prompt):
    """
    You are nature guide that knows about animals and plants. Animals include birds, mammals, reptiles, amphibians, fish, and insects. Plants include trees, flowers, shrubs, grasses, and fungi. Your goal is to teach about wetlands plants and animals, who assumes learners have a 10-second attention span.
    You do not encourage observers to get closer or provide evaluation of the wetland environment, plants or animals. 
    Instead, process one image and text prompt using the LLaMA Vision model. Find one organism in the image and identify the species of the animal or plant in the image. 
    First, provide 3 suggestions for the single plant or animal. Consider the number of times that the user has used the app, when formulating these suggestions. Specifically, newer and irregular users should receive more general suggestions. If the species is unclear, then suggest higher taxonomic levels - Genus, Family, etc. At the roughest level, suggestions should be "plant", "animal", or "unknown species". If identification is uncertain, include "unknown species" as the last of the 3 suggestions.
    Second, provide 1 interesting fact related to the taxonomic recommendations that would take a 5th grader about 10 seconds to read. The single fact should be primarily concise and engaging, and secondarily focused on wetlands plants and animals, fresh water, and ecological importance of wetlands. 
    Draw upon reliable nature guide knowledge.

    Args:
        pipe: The loaded Hugging Face pipeline.
        image_path (str): Path to the image file.
        text_prompt (str): Text prompt to describe the image.

    Returns:
        str: The model's response.
    """
    # Example from dog nutrition
    # SYSTEM_PROMPT = (
        # "You are a Veterinary Communication Assistant. Your goal is to improve dog owners'"
        # " conversations with their veterinarian. You do not provide medical advice, diagnoses,"
        # " treatment plans, or product recommendations. Instead, generate 3 simple, educational"
        # " questions the owner can ask their veterinarian. "
        # "Consider the dog's Age and Health Status when formulating these questions. "
        # "Draw upon reliable veterinary knowledge."
        # )

    try:
        # Validate inputs
        if not image_path or not text_prompt:
            raise ValueError("Both image_path and text_prompt must be provided.")

        # Process the input
        result = pipe({"image": image_path, "text": text_prompt})
        return result
    except Exception as e:
        return f"An error occurred during processing: {e}"

def main():
    """
    Main function to demonstrate the usage of the LLaMA Vision pipeline.
    """
    # Example inputs
    image_path = "path/to/image.jpg"  # Replace with the actual image path
    text_prompt = "Describe this image."

    try:
        # Load the pipeline
        pipe = load_pipeline()

        # Process the image and text prompt
        response = process_image_with_llama(pipe, image_path, text_prompt)
        print(response)
    except Exception as e:
        print(f"An error occurred in the main function: {e}")

if __name__ == "__main__":
    main()

# After Thursday (Post-Prototype Phase)
#     This file will remain relevant for handling the model interaction.
#     If you later decide to use an API or external service, you can adapt this file to handle API calls instead of local model execution.

# Recommendation
#     For Thursday, focus on making this file handle local model execution without relying on an API.
#     After Thursday, you can expand or refactor it based on feedback or new requirements.