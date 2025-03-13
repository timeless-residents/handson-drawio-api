"""Main example for the Draw.io API client."""

import sys

from create_simple_diagram import main as create_simple_diagram
from export_to_image import main as export_to_image
from create_datastore_diagram import main as create_datastore_diagram

if __name__ == "__main__":
    # Check if user specified which example to run
    if len(sys.argv) > 1:
        example = sys.argv[1]
        if example == "simple":
            create_simple_diagram()
        elif example == "image":
            export_to_image()
        elif example == "datastore":
            create_datastore_diagram()
        else:
            print(f"Unknown example: {example}")
            print("Available examples: simple, image, datastore")
    else:
        # Run the datastore example by default
        create_datastore_diagram()