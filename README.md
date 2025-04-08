# Healing Stones - Reconstructing digitized cultural heritage artifacts with artificial intelligence
 Healing Stones is a 3D reconstruction project focused on digitally restoring fragmented cultural artifacts using AI and geometry-based techniques. The goal is to reassemble broken stone pieces—believed to have historical or spiritual significance—into their original form, preserving both structure and meaning.  Using 3D scans of stone fragments (in .PLY format), the project employs:  Automated fragment alignment based on surface geometry and dominant plane detection  Feature extraction using descriptors like FPFH  Graph-based matching and optimization to determine the correct placement of each piece  Deep learning models to improve fragment pair matching and reconstruction accuracy  This pipeline allows for the healing and digital restoration of stone artifacts where physical restoration may not be possible, enabling further archaeological analysis, educational exploration, and cultural preservation.
 
 
 
The entire reconstruction pipeline can be run using the main_run.py script. Executing it will automatically run all the steps in sequence.



Note: This is not the final version of the project. Several challenges were encountered during development, such as RAM overload and Blender crashing while handling large .ply files.

If main_run.py fails to execute properly, please run the individual scripts manually in the order specified by their filenames — they are numbered to indicate the correct sequence.

Important: 6_weighted_graphh.py may take some time to execute. When run through main_run.py, its output might not be visible, but executing it separately will display the progress and results.

The current output may not be perfect or fully optimized, but there is significant room for tweaking and fine-tuning. I am fully committed to addressing these challenges and improving the pipeline throughout the GSoC timeline.
