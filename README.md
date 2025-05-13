# Tkinter File Processor Suite

A simple desktop application built with Python and Tkinter providing tools to process files within a selected directory structure. Useful for compiling source code, exporting file paths, or selectively gathering content from specific files into single output files.

## Features

*   **Tabbed Interface:** Organizes different file processing tools into separate tabs.
*   **Shared Root Directory:** Set a single root directory that applies to all tools.
*   **Source Compiler:**
    *   Recursively walks through the root directory.
    *   Concatenates the content of found files into a single `compiled_sources.txt` file.
    *   Optionally exclude files based on their extensions (comma-separated).
    *   Optionally exclude specific sub-directories (relative paths, comma-separated).
    *   Includes relative paths as headers for each file's content in the output.
    *   Provides a utility to scan and list all unique file extensions found within the (non-excluded) directory structure.
*   **Path Exporter:**
    *   Recursively walks through the root directory.
    *   Exports a list of all found file paths (relative to the root) into `exported_paths.txt`.
    *   Optionally exclude specific sub-directories (relative paths, comma-separated).
*   **Selective Exporter:**
    *   Takes a list of relative file paths (one per line) as input.
    *   Reads the content of each specified file (if it exists within the root directory).
    *   Concatenates the content of these specific files into `selectively_exported_files.txt`.
    *   Includes relative paths as headers for each file's content in the output.
*   **Status Logging:** Each tab provides real-time feedback on the process within its own status area.
*   **Cross-Platform Path Handling:** Uses path normalization (`/`) internally and for output.
*   **Auto-Saving:** Output files are automatically generated and saved in the directory where the Python script is executed.

<!-- Optional: Add a screenshot here -->
<!-- ![Screenshot](path/to/screenshot.png) -->

## Requirements

*   Python 3.x
*   Tkinter (usually included with standard Python installations on Windows/macOS, may need separate installation on Linux, e.g., `sudo apt-get install python3-tk`)

## How to Use

1.  **Clone or Download:** Get the `your_script_name.py` file (replace `your_script_name.py` with the actual filename you save the code as).
2.  **Run the Script:** Open a terminal or command prompt, navigate to the directory where you saved the file, and run:
    ```bash
    python your_script_name.py
    ```
3.  **Set Root Directory:**
    *   Click the "Browse..." button in the "Shared Settings" section at the top.
    *   Select the main folder containing the files you want to process. This is crucial for all operations.
4.  **Select a Tab:** Click on the tab corresponding to the task you want to perform ('Source Compiler', 'Path Exporter', or 'Selective Exporter').

### Using the 'Source Compiler' Tab

1.  **(Optional) Exclude Extensions:** Enter file extensions (without the dot, comma-separated, e.g., `log, tmp, png, jpg`) in the "Exclude Extensions" field if you want to skip files of these types.
2.  **(Optional) Exclude Directories:** Enter relative directory paths (comma-separated, using `/` as separator, e.g., `venv, .git, build, dist/subdir`) in the "Exclude Dirs" field to skip entire directories and their contents.
3.  **(Optional) Get All Extensions:** Click "Get All Extensions" to scan the selected root directory (respecting excluded directories) and list unique extensions found in the status area. This can help decide which extensions to exclude.
4.  **Compile:** Click the `Compile Sources to compiled_sources.txt` button.
5.  **Output:** The application will process the files and create `compiled_sources.txt` in the same directory where you ran the script. The status area will show progress and completion messages.

### Using the 'Path Exporter' Tab

1.  **(Optional) Exclude Directories:** Enter relative directory paths (comma-separated, using `/` as separator, e.g., `__pycache__, node_modules, target`) in the "Exclude Dirs" field to skip listing paths from these directories.
2.  **Export Paths:** Click the `Export Paths to exported_paths.txt` button.
3.  **Output:** The application will list all file paths (respecting exclusions) and create `exported_paths.txt` in the same directory where you ran the script.

### Using the 'Selective Exporter' Tab

1.  **Enter File Paths:** In the large text box, paste or type the relative paths of the files you want to export, one path per line (using `/` as the separator). These paths must be relative to the selected Root Directory. Example:
    ```
    src/main.py
    lib/utils.py
    data/config.json
    README.md
    ```
2.  **Export Selected:** Click the `Export Selected to selectively_exported_files.txt` button.
3.  **Output:** The application will attempt to read each listed file and create `selectively_exported_files.txt` containing their content in the script's execution directory. The status area will report successes, skips (file not found), and errors.

## Output Files

All output files are generated in the **current working directory** (the directory from which you launched the Python script), not necessarily the selected Root Directory.

*   `compiled_sources.txt`: Contains the concatenated content of files processed by the Source Compiler.
*   `exported_paths.txt`: Contains the list of relative file paths generated by the Path Exporter.
*   `selectively_exported_files.txt`: Contains the concatenated content of files specified in the Selective Exporter.

## Notes

*   Directory and extension exclusions are case-insensitive for extensions and path-separator-agnostic for directories due to normalization.
*   The application uses UTF-8 encoding for reading and writing files. `errors='surrogateescape'` is used during reading to handle potential encoding issues gracefully, replacing problematic bytes with placeholders.
*   Performance may vary depending on the size and number of files in the selected root directory. Large directories might take some time to process.