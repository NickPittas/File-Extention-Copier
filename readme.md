# File Extension Copier

A simple GUI application that lets you copy files with specific extensions from a source directory to a destination directory, preserving the folder structure.

![File Extension Copier](https://via.placeholder.com/800x600?text=File+Extension+Copier)

## Features

- Select source and destination folders through an intuitive interface
- Copy only files with specific extensions
- Add and remove extensions from the list
- Preserves original folder structure in the destination
- Real-time progress tracking
- Detailed status updates
- Multi-threaded operation to keep UI responsive
- Cancel operation at any time

## Use Cases

- Backing up specific file types from a project
- Collecting all Nuke script files (`.nk` and `.autosave`) from a complex project structure
- Creating a clean copy of a project with only certain file types

## Installation

### Requirements

- Python 3.6 or higher
- Tkinter (usually comes with Python)

### Setup

1. Clone or download this repository:
   ```
   git clone https://github.com/yourusername/file-extension-copier.git
   cd file-extension-copier
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   python file-copier-ui.py
   ```

## Usage

1. **Select Source Folder**
   - Click "Browse" next to "Source Folder" to select the directory containing your files

2. **Select Destination Folder**
   - Click "Browse" next to "Destination Folder" to select where files should be copied to

3. **Manage Extensions**
   - The tool comes with `.nk` and `.autosave` extensions pre-configured
   - To add a new extension: 
     - Type the extension in the "Add Extension" field (with or without the leading dot)
     - Click "Add"
   - To remove an extension:
     - Select it in the list
     - Click "Remove Selected"

4. **Start Copy Operation**
   - Click "Start Copying" to begin the process
   - The progress bar will show completion percentage
   - The status text area will display real-time updates
   - You can cancel the operation at any time by clicking "Cancel"

## How It Works

The application:
1. Scans the source directory recursively for files with matching extensions
2. Creates the same folder structure in the destination directory
3. Copies each matching file, preserving metadata and timestamps
4. Updates the progress bar and status text as it works

## Troubleshooting

- **No files copying**: Verify your extensions are correct and that matching files exist in the source directory
- **Operation seems stuck**: For very large file operations, the initial file counting might take some time
- **Permission errors**: Ensure you have read access to the source location and write access to the destination

## License

This project is licensed under the MIT License - see the LICENSE file for details.
