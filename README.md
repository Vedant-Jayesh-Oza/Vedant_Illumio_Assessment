# Network Flow Log Analyzer  

## **Project Overview**  
This project processes network flow logs, assigns meaningful tags based on a lookup table, and generates a summary report. It includes a **CLI tool** for log analysis and a **Flask-based Web UI** for user-friendly input submission.  

---

## **Assumptions Made**  
- The input flow log file (`flow_logs.txt`) follows the standard AWS VPC Flow Logs format.  
- The lookup table file (`lookup.txt`) contains three comma-separated columns: `dstport, protocol, tag`.  
- The program supports **TCP, UDP, and ICMP protocols** (mapped from their respective numbers).  
- Any log entry that does not match the lookup table is assigned the tag `"Untagged"`.  
- The output summary is stored in `output/summary.txt`. 
- The program only supports default log format, not custom and the only version that is supported is 2.  

---

## **How to Run the Program (CLI Mode)**  
To execute the program from the **command line interface (CLI):**  

1. **Navigate to the project directory:**  
   ```sh
   cd /path/to/project-directory
2. **Run the main script to generate the summary:**  
   ```sh
   python3 src/main.py
3. **To explicitly run the unit tests:**
   ```sh
   python -m unittest src/test_main.py -v
4. Modify Input Files (Optional): 

   Edit `data/flow_logs.txt` and `data/lookup.txt` to provide custom input data.

## **How to Use the Web Interface**
For a web-based UI to upload files and analyze logs:

1. **Install Flask (if not installed):**  
   ```sh
   pip install flask
2. **Start the Flask Web Server::**  
   ```sh
   python web/app.py
3. **Access the Web App:**
   ```sh
   Open http://127.0.0.1:5000 in a browser.
4. Upload:
   
   Flow Logs File → flow_logs.txt

   Lookup Table File → lookup.txt

   Click "Process Files" to see the analysis results.

## **Tests Performed**

The project includes a test suite to ensure correctness and efficiency:

✔️ Lookup Table Loading Test – Verifies correct mapping of destination ports to tags.

✔️ Flow Log Processing Test – Ensures logs are enriched correctly.

✔️ Large File Handling Test – Processes large input files without memory issues.

✔️ Protocol Handling Test – Validates TCP, UDP, and ICMP protocol identification.

**Run Tests**

To explicitly run the unit tests, use the following command:
```sh
python -m unittest src/test_main.py -v
```

## **Code Analysis & Features**

- Modular Design: Separate functions for lookup table processing, log parsing, and summary generation.

- Error Handling: Warnings for missing files or malformed lines.

- Efficiency: Uses dictionaries for fast lookup and default dictionaries for aggregation.

- Web UI Integration: Allows file uploads for ease of use.


## Example Outputs Video 


https://github.com/user-attachments/assets/81be4e32-e0b7-4fc7-b130-24bb48c6c93b


