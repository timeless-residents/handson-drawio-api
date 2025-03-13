# Draw.io API Hands-on

A practical hands-on project for working with the Draw.io API to programmatically create, modify, and export diagrams.

## Overview

This project demonstrates how to use the Draw.io API to:
- Create diagrams programmatically
- Modify existing diagrams
- Export diagrams to JSON and XML formats
- Export diagrams to image formats (PNG, JPG, SVG, PDF)
- Export diagrams to native Draw.io (.drawio) format
- Customize image exports (transparent background, scaling, custom colors)
- Create program flowcharts from Python code

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

# For image export (PNG, JPG, PDF) support, also install:
pip install cairosvg Pillow
```

## Usage

Check the `examples` directory for various usage examples:

```bash
# Create a simple flowchart and export to JSON
python examples/create_simple_diagram.py

# Create a flowchart with a data store component
python examples/create_datastore_diagram.py

# Export diagram to various image formats (PNG, JPG, SVG, PDF)
python examples/export_to_image.py

# Use the main.py with arguments
python examples/main.py simple     # Run the simple flowchart example
python examples/main.py datastore  # Run the data store diagram example
python examples/main.py image      # Run the image export example
python examples/main.py drawio     # Run the Draw.io format export example

# Generate a flowchart of a Python program
python main_flowchart.py           # Creates a flowchart of main.py program flow
```

## Project Structure

```
handson-drawio-api/
├── examples/                # Example scripts
├── src/                     # Source code
│   └── drawio_api/          # Main package
├── tests/                   # Test suite
├── main_flowchart.py        # Example script to create a flowchart of main.py
├── main_program_flow.drawio # Generated flowchart in Draw.io format
├── main_program_flow.png    # Generated flowchart in PNG format
├── main_program_flow.svg    # Generated flowchart in SVG format
├── README.md
└── requirements.txt
```

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.