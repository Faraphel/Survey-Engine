# Survey Engine

This is a small engine for the survey created for one of our master projet.  
It allows for a small survey embedding a web page to track the user input allowing for metrics collection.  
This run with the [PyQt6](https://www.riverbankcomputing.com/software/pyqt/) and 
[PyQt6-WebEngine](https://www.riverbankcomputing.com/software/pyqtwebengine/) librairies. 

# Installation

To install the projet, you will need to install :

- Python >= 3.11 (preferably in a virtual environment with `python3 -m venv ./.venv/`)
- Python dependencies (`python3 -m pip install -r ./requirements.txt`)

Or download one of the build in the [releases page](https://github.com/Faraphel/M1-Recherche/releases).

# Run

You can run the projet simply by using the command `python3 main.py`.  
A window will then open containing the survey. Once the survey finished, a file containing all the data
will be created in the `./results/` directory.  
If configured properly, the result can also be automatically sent to a discord webhooks.
