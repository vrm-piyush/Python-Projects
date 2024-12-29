# QR Code Generator Program

![qr code](../../assets/images/readme_images/QR_code_generator.png)

## Project Overview

The QR Code Generator Program is a Python implementation that allows users to generate QR codes from text or URLs with various features. The program supports both single QR code generation and batch processing for multiple QR code generations. Users can choose the error correction level, embed a logo or image in the QR code, and customize the size and output format.

## Features

- **Single QR Code Generation:**

  - Users can generate a single QR code by providing the type of data (Text or URL), the data itself, error correction level, output filename, logo embedding, size adjustment, and output format.

- **Batch Processing:**

  - Users can perform batch processing by reading data from a batch file containing multiple entries for QR code generation. Each entry includes data, output filename, error correction level, logo embedding, size adjustment, and output format.

- **Data Validation:**

  - Validates user-provided data based on the chosen data type (Text or URL) before generating QR codes.

- **Logo Embedding:**

  - Option to embed a logo or image in the center of the QR code for branding purposes.

- **Error Correction Level:**

  - Users can choose the error correction level ('L', 'M', 'Q', or 'H') for the generated QR code.

- **Size Adjustment:**

  - Allows users to adjust the size (dimensions) of the generated QR code.

- **Output Formats:**
  - Supports different output formats for the QR code image, including PNG and EPS.

## How to Use

1. **Run the Program:**

   - Execute the program to choose between single QR code generation and batch processing.

2. **Single QR Code Generation:**

   - Provide details for generating a single QR code, including data type, data, error correction level, output filename, logo embedding, size adjustment, and output format.

3. **Batch Processing:**

   - Create a batch file with entries for multiple QR code generations. Each entry should include data, output filename, error correction level, logo embedding, size adjustment, and output format.

4. **Data Validation:**

   - Ensure that the provided data is valid based on the chosen data type (Text or URL).

5. **Logo Embedding:**

   - Optionally embed a logo or image in the center of the QR code for branding.

6. **Error Correction Level:**

   - Choose the error correction level for the QR code to determine fault tolerance.

7. **Size Adjustment:**

   - Adjust the size of the generated QR code.

8. **Output Formats:**

   - Choose the desired output format for the QR code image, such as PNG or EPS.

9. **Batch Processing Mode:**

   - For batch processing, provide a batch file with entries for each QR code generation.

10. **Logo Embedding:**
    - Optionally embed a logo or image in the center of the QR code for branding purposes.

## Example

```bash
cd QRCodeGenerator
python qr_code_generator.py
```

```python
Mode
1. Single QR Code Generation
2. Batch Processing
Enter your choice: 1

Type of data to encode
1. Text
2. URL
Enter your choice: 1
Enter the data to encode: Hello, World!
Choose the error correction level (L, M, Q, H): M
Enter the output filename (include extension, e.g., output.png): hello_world.png
Enter the path to the logo/image file for embedding (leave empty if none): logo.png
Enter the size adjustment factor (leave empty for default size): 200
Enter the QR code version (leave empty for default version): 5
Choose the output format ('png', 'eps'): png

QR code generated and saved in 'QRCodes' folder as hello_world.png
```

## Features to be Added

- **Custom Colors:**

  - Allow users to customize the colors of the QR code (background and foreground) for a personalized appearance.

- **Bulk Generation:**

  - Enable users to generate multiple QR codes at once by providing a list of data and filenames.

- **Output Formats:**

  - Support additional output formats such as SVG, or other image formats in addition to PNG and EPS.

- **Security Features:**

  - If applicable, consider adding features such as encryption for sensitive data within the QR code.

- **Compression:**

  - Implement compression algorithms to reduce the size of the generated QR code, especially for larger data.

- **QR Code Reading:**

  - Include an option to read and decode QR codes using a built-in or external library.

## Contribution Guidelines

Contributions are welcome! If you have ideas for improvements or encounter any issues, please open an [issue](https://github.com/vrm-piyush/Python-Projects/issues/new/choose) or refer to [contribution guidelines](../../CONTRIBUTING.md) for more details.

---
