import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox, scrolledtext, Text # filedialog still needed for _browse_root_dir
import os

# --- Helper Function ---
def normalize_path(path_str):
    """Normalizes path separators for consistent comparison."""
    return path_str.replace('\\', '/').strip('/')

class MainApp:
    # Predefined output filenames
    COMPILED_SOURCES_FILENAME = "compiled_sources.txt"
    EXPORTED_PATHS_FILENAME = "exported_paths.txt"
    SELECTIVE_EXPORT_FILENAME = "selectively_exported_files.txt"

    def __init__(self, master):
        self.master = master
        master.title("Tabbed File Processor (Auto-Save)")
        master.geometry("750x650") 

        self.root_dir_var = tk.StringVar()

        # --- Top Section: Root Directory ---
        root_settings_frame = tk.LabelFrame(master, text="Shared Settings", padx=10, pady=10)
        root_settings_frame.pack(padx=10, pady=10, fill="x", side=tk.TOP)

        tk.Label(root_settings_frame, text="Root Directory:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.root_dir_entry = tk.Entry(root_settings_frame, textvariable=self.root_dir_var, width=60)
        self.root_dir_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        tk.Button(root_settings_frame, text="Browse...", command=self._browse_root_dir).grid(row=0, column=2, padx=5, pady=5)
        root_settings_frame.grid_columnconfigure(1, weight=1)

        # --- Notebook for Tabbed Interface ---
        self.notebook = ttk.Notebook(master)
        self.notebook.pack(padx=10, pady=10, fill="both", expand=True)

        self.compiler_tab = ttk.Frame(self.notebook, padding=(10, 10))
        self.path_exporter_tab = ttk.Frame(self.notebook, padding=(10, 10))
        self.selective_exporter_tab = ttk.Frame(self.notebook, padding=(10, 10))

        self.notebook.add(self.compiler_tab, text='Source Compiler')
        self.notebook.add(self.path_exporter_tab, text='Path Exporter')
        self.notebook.add(self.selective_exporter_tab, text='Selective Exporter')

        self._create_compiler_ui(self.compiler_tab)
        self._create_path_exporter_ui(self.path_exporter_tab)
        self._create_selective_exporter_ui(self.selective_exporter_tab)
        
        self.notebook.bind("<<NotebookTabChanged>>", self._on_tab_change)


    def _log_status(self, message, target_status_widget, clear_first=False):
        target_status_widget.configure(state='normal')
        if clear_first:
            target_status_widget.delete('1.0', tk.END)
        target_status_widget.insert(tk.END, message + "\n")
        target_status_widget.see(tk.END)
        target_status_widget.configure(state='disabled')
        self.master.update_idletasks()

    def _parse_exclusions(self, var_str, is_extensions=False):
        raw_list = var_str.get().split(',')
        if is_extensions:
            return {f".{ext.strip().lstrip('.').lower()}" for ext in raw_list if ext.strip()}
        else:
            return {normalize_path(d.strip()) for d in raw_list if d.strip()}

    def _browse_root_dir(self):
        directory = filedialog.askdirectory(parent=self.master)
        if directory:
            self.root_dir_var.set(directory)
            print(f"Root directory set to: {directory}") 

    def _check_root_dir_set(self, show_error=True):
        if not self.root_dir_var.get() or not os.path.isdir(self.root_dir_var.get()):
            if show_error:
                messagebox.showerror("Root Directory Not Set", 
                                     "Please select a valid root directory first.", 
                                     parent=self.master)
            return False
        return True
    
    def _on_tab_change(self, event):
        if not self._check_root_dir_set(show_error=False):
            pass

    # --- UI Creation for Compiler Tab ---
    def _create_compiler_ui(self, parent_tab_frame):
        self.compiler_excluded_extensions_var = tk.StringVar()
        self.compiler_excluded_dirs_var = tk.StringVar()

        controls_frame = tk.LabelFrame(parent_tab_frame, text="Compiler Settings", padx=10, pady=10)
        controls_frame.pack(padx=0, pady=0, fill="x")

        tk.Label(controls_frame, text="Exclude Extensions (comma-sep):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        tk.Entry(controls_frame, textvariable=self.compiler_excluded_extensions_var, width=40).grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        tk.Button(controls_frame, text="Get All Extensions", command=self._compiler_get_all_extensions).grid(row=0, column=2, padx=5, pady=5)

        tk.Label(controls_frame, text="Exclude Dirs (relative, comma-sep):").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        tk.Entry(controls_frame, textvariable=self.compiler_excluded_dirs_var, width=40).grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        controls_frame.grid_columnconfigure(1, weight=1)

        tk.Button(parent_tab_frame, text=f"Compile Sources to {self.COMPILED_SOURCES_FILENAME}", command=self._compiler_compile_sources, bg="lightblue").pack(padx=0, pady=5, fill="x")

        status_frame = tk.LabelFrame(parent_tab_frame, text="Compiler Status / Found Extensions", padx=10, pady=10)
        status_frame.pack(padx=0, pady=5, fill="both", expand=True)
        self.compiler_status_text = scrolledtext.ScrolledText(status_frame, height=10, wrap=tk.WORD)
        self.compiler_status_text.pack(fill="both", expand=True)
        self.compiler_status_text.configure(state='disabled')

    # --- UI Creation for Path Exporter Tab ---
    def _create_path_exporter_ui(self, parent_tab_frame):
        self.path_exporter_excluded_dirs_var = tk.StringVar()

        controls_frame = tk.LabelFrame(parent_tab_frame, text="Path Exporter Settings", padx=10, pady=10)
        controls_frame.pack(padx=0, pady=0, fill="x")

        tk.Label(controls_frame, text="Exclude Dirs (relative, comma-sep):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        tk.Entry(controls_frame, textvariable=self.path_exporter_excluded_dirs_var, width=40).grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        controls_frame.grid_columnconfigure(1, weight=1)

        tk.Button(parent_tab_frame, text=f"Export Paths to {self.EXPORTED_PATHS_FILENAME}", command=self._path_exporter_export_paths, bg="lightgreen").pack(padx=0, pady=5, fill="x")

        status_frame = tk.LabelFrame(parent_tab_frame, text="Path Exporter Status", padx=10, pady=10)
        status_frame.pack(padx=0, pady=5, fill="both", expand=True)
        self.path_exporter_status_text = scrolledtext.ScrolledText(status_frame, height=8, wrap=tk.WORD)
        self.path_exporter_status_text.pack(fill="both", expand=True)
        self.path_exporter_status_text.configure(state='disabled')

    # --- UI Creation for Selective Exporter Tab ---
    def _create_selective_exporter_ui(self, parent_tab_frame):
        input_area_frame = tk.LabelFrame(parent_tab_frame, text="Files to Export (Relative Paths, One Per Line)", padx=10, pady=10)
        input_area_frame.pack(padx=0, pady=0, fill="both", expand=True)

        self.selective_exporter_file_list_text = Text(input_area_frame, height=15, width=70, wrap=tk.WORD)
        scrollbar = tk.Scrollbar(input_area_frame, command=self.selective_exporter_file_list_text.yview)
        self.selective_exporter_file_list_text.config(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=(0,5))
        self.selective_exporter_file_list_text.pack(pady=(0,5), fill="both", expand=True, side=tk.LEFT)

        tk.Button(parent_tab_frame, text=f"Export Selected to {self.SELECTIVE_EXPORT_FILENAME}", command=self._selective_exporter_export_files, bg="lightyellow").pack(padx=0, pady=5, fill="x", side=tk.TOP)

        status_frame = tk.LabelFrame(parent_tab_frame, text="Selective Exporter Status", padx=10, pady=10)
        status_frame.pack(padx=0, pady=5, fill="both", expand=True, side=tk.TOP)
        self.selective_exporter_status_text = scrolledtext.ScrolledText(status_frame, height=8, wrap=tk.WORD)
        self.selective_exporter_status_text.pack(fill="both", expand=True)
        self.selective_exporter_status_text.configure(state='disabled')


    # --- Logic for Compiler ---
    def _compiler_get_all_extensions(self):
        if not self._check_root_dir_set(): return
        root_dir = self.root_dir_var.get()
        excluded_dirs_set = self._parse_exclusions(self.compiler_excluded_dirs_var)
        
        self._log_status("Scanning for extensions...", self.compiler_status_text, clear_first=True)
        found_extensions_data = {} 
        files_scanned = 0
        
        try:
            for dirpath, dirnames, filenames in os.walk(root_dir, topdown=True):
                current_rel_dir_path = normalize_path(os.path.relpath(dirpath, root_dir))
                if current_rel_dir_path == '.': current_rel_dir_path = ""

                original_dirnames = list(dirnames) 
                dirnames[:] = [] 
                for d_name in original_dirnames:
                    subdir_rel_path = normalize_path(os.path.join(current_rel_dir_path, d_name))
                    is_excluded = any(subdir_rel_path == ex_dir or subdir_rel_path.startswith(ex_dir + '/') for ex_dir in excluded_dirs_set if ex_dir)
                    if not is_excluded:
                        dirnames.append(d_name)

                is_current_dir_excluded = any(current_rel_dir_path == ex_dir or (current_rel_dir_path.startswith(ex_dir + '/') and ex_dir) for ex_dir in excluded_dirs_set if ex_dir)
                if is_current_dir_excluded:
                    self._log_status(f"Skipping excluded directory: {current_rel_dir_path or '(root level excluded dir)'}", self.compiler_status_text)
                    continue

                for filename in filenames:
                    files_scanned += 1
                    relative_path_normalized = normalize_path(os.path.join(current_rel_dir_path, filename))
                    _, ext = os.path.splitext(filename)
                    ext = ext.lower()
                    if ext:
                        if ext not in found_extensions_data:
                            found_extensions_data[ext] = []
                        if len(found_extensions_data[ext]) < 3:
                            found_extensions_data[ext].append(relative_path_normalized)
            
            if found_extensions_data:
                log_message = "Found extensions (up to 3 examples each, from non-excluded directories):\n"
                for ext_key in sorted(found_extensions_data.keys()):
                    log_message += f"\n{ext_key}:\n"
                    for example_path in found_extensions_data[ext_key]:
                        log_message += f"  - {example_path}\n"
                self._log_status(log_message, self.compiler_status_text)
            else:
                self._log_status("No files with extensions found in non-excluded directories.", self.compiler_status_text)
            self._log_status(f"Total files scanned (in non-excluded dirs): {files_scanned}", self.compiler_status_text)
        except Exception as e:
            messagebox.showerror("Error", f"Error scanning extensions: {e}", parent=self.master)
            self._log_status(f"Error scanning extensions: {e}", self.compiler_status_text)


    def _compiler_compile_sources(self):
        if not self._check_root_dir_set(): return
        
        output_filename = self.COMPILED_SOURCES_FILENAME
        output_filepath = os.path.join(os.getcwd(), output_filename)

        self._log_status(f"Starting source compilation to {output_filepath}...", self.compiler_status_text, clear_first=True)
        root_dir = self.root_dir_var.get()
        excluded_extensions_set = self._parse_exclusions(self.compiler_excluded_extensions_var, is_extensions=True)
        excluded_dirs_set = self._parse_exclusions(self.compiler_excluded_dirs_var)

        files_processed_count = 0
        try:
            with open(output_filepath, 'w', encoding='utf-8', errors='surrogateescape') as outfile:
                for dirpath, dirnames, filenames in os.walk(root_dir, topdown=True):
                    current_rel_dir_path = normalize_path(os.path.relpath(dirpath, root_dir))
                    if current_rel_dir_path == '.': current_rel_dir_path = ""

                    original_dirnames = list(dirnames)
                    dirnames[:] = []
                    for d_name in original_dirnames:
                        subdir_rel_path = normalize_path(os.path.join(current_rel_dir_path, d_name))
                        is_excluded = any(subdir_rel_path == ex_dir or subdir_rel_path.startswith(ex_dir + '/') for ex_dir in excluded_dirs_set if ex_dir)
                        if not is_excluded:
                            dirnames.append(d_name)
                    
                    is_current_dir_excluded = any(current_rel_dir_path == ex_dir or (current_rel_dir_path.startswith(ex_dir + '/') and ex_dir) for ex_dir in excluded_dirs_set if ex_dir)
                    if is_current_dir_excluded:
                        self._log_status(f"Skipping excluded dir: {current_rel_dir_path or '(root level excluded dir)'}", self.compiler_status_text)
                        continue

                    for filename in filenames:
                        _, ext = os.path.splitext(filename)
                        ext = ext.lower()
                        if excluded_extensions_set and ext in excluded_extensions_set:
                            continue
                        
                        full_path = os.path.join(dirpath, filename)
                        relative_path_normalized = normalize_path(os.path.join(current_rel_dir_path, filename))

                        self._log_status(f"Processing: {relative_path_normalized}", self.compiler_status_text)
                        outfile.write(f"--- RELATIVE PATH: {relative_path_normalized} ---\n")
                        try:
                            with open(full_path, 'r', encoding='utf-8', errors='surrogateescape') as infile_content:
                                outfile.write(infile_content.read())
                            outfile.write("\n\n")
                            files_processed_count += 1
                        except Exception as e_read:
                            outfile.write(f"ERROR READING FILE: {e_read}\n\n")
                            self._log_status(f"Error reading {relative_path_normalized}: {e_read}", self.compiler_status_text)
            
            self._log_status(f"Compilation complete. {files_processed_count} file(s) written to {output_filepath}", self.compiler_status_text)
            messagebox.showinfo("Success", f"Compiled {files_processed_count} files to:\n{output_filepath}", parent=self.master)
        except Exception as e:
            messagebox.showerror("Error", f"Error during compilation: {e}\nFile: {output_filepath}", parent=self.master)
            self._log_status(f"Error during compilation: {e}", self.compiler_status_text)

    # --- Logic for Path Exporter ---
    def _path_exporter_export_paths(self):
        if not self._check_root_dir_set(): return

        output_filename = self.EXPORTED_PATHS_FILENAME
        output_filepath = os.path.join(os.getcwd(), output_filename)

        self._log_status(f"Starting path export to {output_filepath}...", self.path_exporter_status_text, clear_first=True)
        root_dir = self.root_dir_var.get()
        excluded_dirs_set = self._parse_exclusions(self.path_exporter_excluded_dirs_var)

        paths_exported_count = 0
        try:
            with open(output_filepath, 'w', encoding='utf-8') as outfile:
                for dirpath, dirnames, filenames in os.walk(root_dir, topdown=True):
                    current_rel_dir_path = normalize_path(os.path.relpath(dirpath, root_dir))
                    if current_rel_dir_path == '.': current_rel_dir_path = ""

                    original_dirnames = list(dirnames)
                    dirnames[:] = []
                    for d_name in original_dirnames:
                        subdir_rel_path = normalize_path(os.path.join(current_rel_dir_path, d_name))
                        is_excluded = any(subdir_rel_path == ex_dir or subdir_rel_path.startswith(ex_dir + '/') for ex_dir in excluded_dirs_set if ex_dir)
                        if not is_excluded:
                            dirnames.append(d_name)

                    is_current_dir_excluded = any(current_rel_dir_path == ex_dir or (current_rel_dir_path.startswith(ex_dir + '/') and ex_dir) for ex_dir in excluded_dirs_set if ex_dir)
                    if is_current_dir_excluded:
                        self._log_status(f"Skipping excluded dir: {current_rel_dir_path or '(root level excluded dir)'}", self.path_exporter_status_text)
                        continue

                    for filename in filenames:
                        relative_path_normalized = normalize_path(os.path.join(current_rel_dir_path, filename))
                        outfile.write(relative_path_normalized + "\n")
                        paths_exported_count += 1
                        if paths_exported_count % 200 == 0:
                             self._log_status(f"Exported {paths_exported_count} paths...", self.path_exporter_status_text)
            
            self._log_status(f"Path export complete. {paths_exported_count} path(s) written to {output_filepath}", self.path_exporter_status_text)
            messagebox.showinfo("Success", f"Exported {paths_exported_count} paths to:\n{output_filepath}", parent=self.master)
        except Exception as e:
            messagebox.showerror("Error", f"Error during path export: {e}\nFile: {output_filepath}", parent=self.master)
            self._log_status(f"Error during path export: {e}", self.path_exporter_status_text)

    # --- Logic for Selective Exporter ---
    def _selective_exporter_export_files(self):
        if not self._check_root_dir_set(): return

        output_filename = self.SELECTIVE_EXPORT_FILENAME
        output_filepath = os.path.join(os.getcwd(), output_filename)
        
        self._log_status(f"Starting selective file export to {output_filepath}...", self.selective_exporter_status_text, clear_first=True)
        root_dir = self.root_dir_var.get()
        
        raw_file_list = self.selective_exporter_file_list_text.get("1.0", tk.END).strip()
        if not raw_file_list:
            messagebox.showwarning("No Files", "Please enter at least one relative file path.", parent=self.master)
            self._log_status("No file paths provided.", self.selective_exporter_status_text)
            return

        relative_paths_to_export = [normalize_path(p.strip()) for p in raw_file_list.splitlines() if p.strip()]

        if not relative_paths_to_export:
            messagebox.showwarning("No Files", "No valid file paths found after processing input.", parent=self.master)
            self._log_status("No valid file paths to process.", self.selective_exporter_status_text)
            return

        files_processed_count = 0
        errors_encountered = 0
        try:
            with open(output_filepath, 'w', encoding='utf-8', errors='surrogateescape') as outfile:
                for rel_path in relative_paths_to_export:
                    full_path = os.path.join(root_dir, rel_path) 
                    normalized_rel_path_for_output = rel_path 

                    if not os.path.isfile(full_path):
                        self._log_status(f"SKIPPING (Not a file or not found): {normalized_rel_path_for_output}", self.selective_exporter_status_text)
                        outfile.write(f"--- SKIPPED (Not a file or not found): {normalized_rel_path_for_output} ---\n\n")
                        errors_encountered +=1
                        continue

                    self._log_status(f"Processing: {normalized_rel_path_for_output}", self.selective_exporter_status_text)
                    outfile.write(f"--- RELATIVE PATH: {normalized_rel_path_for_output} ---\n")
                    try:
                        with open(full_path, 'r', encoding='utf-8', errors='surrogateescape') as infile_content:
                            outfile.write(infile_content.read())
                        outfile.write("\n\n")
                        files_processed_count += 1
                    except Exception as e_read:
                        outfile.write(f"ERROR READING FILE ({normalized_rel_path_for_output}): {e_read}\n\n")
                        self._log_status(f"Error reading {normalized_rel_path_for_output}: {e_read}", self.selective_exporter_status_text)
                        errors_encountered +=1
            
            summary_message = f"Selective export complete. {files_processed_count} file(s) successfully written."
            if errors_encountered > 0:
                summary_message += f" {errors_encountered} file(s) had issues (see log)."
            self._log_status(f"{summary_message} Output: {output_filepath}", self.selective_exporter_status_text)
            messagebox.showinfo("Success", f"{summary_message}\nOutput saved to:\n{output_filepath}", parent=self.master)

        except Exception as e:
            messagebox.showerror("Error", f"Error during selective export: {e}\nFile: {output_filepath}", parent=self.master)
            self._log_status(f"Error during selective export: {e}", self.selective_exporter_status_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()