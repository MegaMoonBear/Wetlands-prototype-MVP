import ollama

response = ollama.chat(
    model='llama3.2-vision',
    messages=[{
        'role': 'user',
        'content': 'What is in this image?',
        'images': ['C:\\Users\\Meghan Carr\\Desktop\\Meghan - ALL til OneDrive\\5-0 - Portfolio Projects\\Wetland\\Water prototype\\Wetlands-prototype-MVP\\backend\\sandbox\\images\\BirdsFromBelow.jpg']
    }]
)

print(response)