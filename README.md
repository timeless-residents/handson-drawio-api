# Draw.io API Hands-on

A practical hands-on project for working with the Draw.io API to programmatically create, modify, and export diagrams.

## Overview

This project demonstrates how to use the Draw.io API to:
- Create diagrams programmatically
- Modify existing diagrams
- Export diagrams to JSON and XML formats
- Export diagrams to image formats (PNG, JPG, SVG, PDF)
- Customize image exports (transparent background, scaling, custom colors)

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/handson-drawio-api.git
cd handson-drawio-api

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

Check the `examples` directory for various usage examples:

```bash
# Export diagram to JSON format
python examples/create_simple_diagram.py

# Export diagram to various image formats (PNG, JPG, SVG, PDF)
python examples/export_to_image.py

# Use the main.py with arguments
python examples/main.py json   # Run the JSON export example
python examples/main.py image  # Run the image export example
```

## Project Structure

```
handson-drawio-api/
├── examples/          # Example scripts
├── src/               # Source code
│   └── drawio_api/    # Main package
├── tests/             # Test suite
├── README.md
└── requirements.txt
```

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.