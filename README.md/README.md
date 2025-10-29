Image Forgery Detection using Digital Forensics Techniques
 Cyber Security Mini Project | Built with Python, OpenCV, scikit-learn, and Streamlit
 Project Overview

With the growing prevalence of image manipulation, verifying the authenticity of digital images has become critical in digital forensics and cyber security.
This project presents an Image Forgery Detection System capable of detecting tampered or manipulated regions within an image using EXIF metadata analysis, Error Level Analysis (ELA), and Copy–Move forgery detection techniques.

It provides a complete, automated forensic report that visualizes suspected forgeries and metadata inconsistencies, assisting investigators, journalists, and forensic professionals in determining the originality of an image.

 Key Features

EXIF Metadata Extraction – Extracts hidden metadata (camera details, timestamps, GPS, editing software, etc.) using the exifread library.
Error Level Analysis (ELA) – Highlights regions with inconsistent compression levels using pixel-level difference visualization.
Copy–Move Forgery Detection – Detects cloned areas using SIFT/ORB keypoint matching and dense correlation analysis.
Automated Report Generation – Creates an interactive HTML report with all results (EXIF data, ELA map, Copy–Move mask).
Modular & Extensible – Designed for easy integration with deep learning–based forgery detection or video frame analysis.

 Project Workflow
          ┌────────────────────────┐
          │      Input Image       │
          └──────────┬─────────────┘
                     │
                     ▼
          ┌────────────────────────┐
          │  EXIF Metadata Reader  │  →  Extracts hidden info
          └──────────┬─────────────┘
                     │
                     ▼
          ┌────────────────────────┐
          │  Error Level Analysis  │  →  Highlights tampered areas
          └──────────┬─────────────┘
                     │
                     ▼
          ┌────────────────────────┐
          │ Copy–Move Detection    │  →  Finds cloned objects
          └──────────┬─────────────┘
                     │
                     ▼
          ┌────────────────────────┐
          │  Forensic HTML Report  │  →  Combines all results
          └────────────────────────┘

 Tech Stack
Component	Technology Used
Language	Python 3.10+
Libraries	OpenCV, NumPy, scikit-learn, Pillow, ExifRead, Jinja2
Output Format	HTML Report with Embedded Results
Optional UI	Streamlit (for real-time web-based demo)
 Installation & Setup
 Clone the repository
git clone https://github.com/<your-username>/Image-Forensics-Detection.git
cd Image-Forensics-Detection

 Create and activate a virtual environment

For Windows (PowerShell):

python -m venv .venv
& ".venv/Scripts/Activate.ps1"


For Git Bash:

python -m venv .venv
source .venv/Scripts/activate

 Install dependencies
pip install -r requirements.txt

 Run the project
python src/main.py "data/sample.jpg"


The output will be generated inside the /out folder, and a forensic report (report.html) will open automatically in your browser.

 Modules Description
🔹 exif_tools.py

Extracts and displays EXIF metadata such as camera model, GPS coordinates, and editing software used.
Used to verify the image’s authenticity and trace its origin.

🔹 ela.py

Performs Error Level Analysis by resaving the image at 90% quality, subtracting it from the original, and visualizing areas with inconsistent compression levels.

🔹 copymove.py

Detects cloned regions using:

SIFT/ORB feature extraction

DBSCAN clustering

Delaunay triangulation

Dense correlation matching (ZNCC) for low-texture areas.

🔹 main.py

Acts as the controller — combines results from all modules, generates the final forensic report, and saves output files to the /out directory.

 Sample Output
Stage	Description	Output
EXIF Metadata	Extracted data fields	

ELA Map	Bright areas indicate tampering	

Copy–Move Detection	Red boxes/triangles mark cloned areas	

Final Report	HTML forensic summary	
 Results and Outcome

The developed system successfully:

Detected metadata inconsistencies using EXIF data

Highlighted possible tampering through ELA visualization

Identified duplicated or cloned objects using feature and block-based correlation methods

Generated an integrated forensic report that consolidates analytical and visual results

The approach demonstrates the real-world feasibility of automated image integrity verification, making it a valuable asset for journalists, investigators, and cybersecurity professionals.

 Future Scope

Integrate deep learning models (e.g., CNN or Vision Transformers) for semantic forgery detection
Extend support to video frame analysis for video forensics
Implement noise inconsistency and shadow analysis techniques
Deploy the system as a full-fledged web app using Streamlit or Flask
Integrate cloud-based storage for large-scale image authentication

References

A.C. Popescu and H. Farid, “Exposing Digital Forgeries by Detecting Duplicated Image Regions,” Dartmouth College Technical Report TR2004-515.

Jessica Fridrich et al., “Detection of Copy-Move Forgery in Digital Images,” DFRWS, 2003.

OpenCV Documentation – https://docs.opencv.org

scikit-image Documentation – https://scikit-image.org

ExifRead Library – https://pypi.org/project/ExifRead/

Pillow (PIL) Documentation – https://pillow.readthedocs.io

Author

Aditi Rathi
Cyber Security & Digital Forensics Enthusiast
PES Modern College of Engineering, Pune
📧 aditirathi340@gmail.com
🔗 linkedin: @aditirathi33