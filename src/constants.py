# Timing constants (in seconds)
IOS_LOAD_TIME = 0.5
CBCT_LOAD_TIME = 1.0
IOS_SEGMENTATION_TIME = 7.0  # Simulating 5-10 seconds
CBCT_TEETH_SEGMENTATION_TIME = 20.0  # Part of the 1-minute process
CBCT_GUM_DETECTION_TIME = 15.0  # Part of the 1-minute process
CBCT_NERVE_DETECTION_TIME = 25.0  # Part of the 1-minute process
ALIGNMENT_TIME = 15.0
CROWN_DESIGN_TIME = 30.0

# Metadata constants
IOS_FILE_EXTENSION = ".stl"
CBCT_FILE_EXTENSION = ".dcm"
OUTPUT_FILE_EXTENSION = ".obj"

# Group names for organizing assets
GROUP_INPUT = "input_files"
GROUP_SEGMENTATION = "segmentation_processes"
GROUP_OUTPUT = "final_outputs"