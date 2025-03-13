# Draw.io API Hands-on

A practical hands-on project for working with the Draw.io API to programmatically create, modify, and export diagrams.

## Overview

This project demonstrates how to use the Draw.io API to:
- Create diagrams programmatically
- Modify existing diagrams
- Export diagrams to various formats
- Import diagrams from other sources

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
python examples/create_simple_diagram.py
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