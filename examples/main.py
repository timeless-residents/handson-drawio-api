"""Main example for the Draw.io API client."""

import sys

from create_simple_diagram import main as create_simple_diagram
from export_to_image import main as export_to_image

if __name__ == "__main__":
    # Check if user specified which example to run
    if len(sys.argv) > 1:
        example = sys.argv[1]
        if example == "json":
            create_simple_diagram()
        elif example == "image":
            export_to_image()
        else:
            print(f"Unknown example: {example}")
            print("Available examples: json, image")
    else:
        # Run the export_to_image example by default
        export_to_image()