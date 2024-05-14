# ShortStory Generator

![story generator](image.png)

## Project Overview

The ShortStory Generator is a Python program that generates random stories based on predefined lists. Users can choose the type of story they want to generate, such as mystery, adventure, romance, or fantasy. The program dynamically fills in a story template with randomly chosen elements from the selected scenario's lists. It also provides options to save the generated story to a file.

## Features

- **Scenario Selection:**

  - Users can choose the type of story (scenario) they want to generate.

- **Predefined Lists:**

  - The program includes predefined lists for different scenarios, including mystery, adventure, romance, and fantasy.

- **Dynamic ShortStory Filling:**

  - Dynamically fills in a story template with randomly chosen elements from the selected scenario's lists.

- **Text Formatting:**

  - Capitalizes the first letter of the story.
  - Adds a period at the end if missing.

- **Save Option:**

  - Gives users the option to save the generated story to a file.

- **User Input Validation:**

  - Validates user choices and handles invalid inputs gracefully.

- **Extensibility:**
  - Easily extensible by adding more scenarios and lists.

## How to Use

1. **Run the Program:**

   - Execute the program and follow the on-screen prompts.

2. **Choose Scenario:**

   - Choose the type of story you want to generate from the available scenarios.

3. **Generated Short Story:**

   - The program generates a random story and displays it to the user.

4. **Save:**
   - Optionally, choose to save the story to a file.

## Example

```bash
cd ShortStoryGenerator
python short_story_generator.py
```

```python
Choose the type of story:
1. Mystery
2. Adventure
3. Romance
4. Fantasy
Enter the number of your choice: 2

Here is your adventure story:
During a celestial alignment, a dragon rider named Drakon, who lived in an enchanted tower, went to an enchanted castle and found a legendary artifact.

Do you want to save this story to a file? (yes/no): yes
ShortStory saved to adventure.txt
```

## Features to be Added

- **Sharing on Social Media:**

  - Implement the ability to share the generated story on social media.

- **More Scenarios and Lists:**

  - Extend the program by adding more scenarios and lists for a diverse range of story options.

- **Improved User Interface:**

  - Enhance the user interface for a more engaging experience.

- **Error Handling:**

  - Implement comprehensive error handling for various scenarios.

- **Story Customization:**
  - Allow users to customize certain elements of the generated story.

## Contribution Guidelines

Contributions are welcome! If you have ideas for improvements or encounter any issues, please open an [issue](https://github.com/vrm-piyush/Acronym/issues) or refer to [contribution guidelines](../CONTRIBUTING.md) for more details.

---