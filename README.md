<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a id="readme-top"></a>

<!-- PROJECT SHIELDS -->
<!--
*** Using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Stargazers][stars-shield]][stars-url]
[![GPL License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]
[![LinkedIn][linkedin-shield1]][linkedin-url1]

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/rjandaya/vpambu-ctc-report-generator">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>
  <h3 align="center">Viewpoint Ambulance Billing Invoice Report Tool</h3>
  <p align="center">
    Program that merges data from two unique datasets into a comprehensive billing report.
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project

This project involves creating a main script to process and merge data from two CSV files to generate comprehensive billing reports. The script performs the following steps:

1. **Load Data**: Imports two CSV files containing data from Traumasoft and Call the Car (CTC) records.
2. **Clean Data**: Removes trailing NaN rows in Traumasoft data.
3. **Extract Information**: Retrieves wait time and oxygen requirement from Call the Car (CTC) data.
4. **Standardize Addresses**: Normalizes address formats and creates combined address columns.
5. **Merge Data**: Combines the datasets based on 'Patient Name', 'Date of Service', and 'PU Address'.
6. **Select Columns**: Focuses on specific columns for the final billing report.
7. **Save Output**: Exports the merged data to a CSV file in the output directory.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

![Python-url][Python]

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

To get started with this program, ensure you have <a href="https://www.python.org/downloads/">Python</a> installed.

### Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/rjandaya/vpambu-ctc-report-generator.git
   ```
2. Create a virtual environment:
   ```sh
   python -m venv venv
   ```
3. Activate the virtual environment:
   - On Windows:
     ```sh
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```sh
     source venv/bin/activate
     ```
4. Install the required packages:
   ```sh
   pip install -r requirements.txt
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->
## Usage

First, copy all `.csv` files into the `input` directory.

Example:
```sh
python main.py
```
This will automatically process all files in the `input` directory.

Or specify individual files:
```sh
python main.py "file1.csv" "file2.csv"
```
The final billing report will be saved to the `output` directory.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- LICENSE -->
## License

Distributed under the GNU License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTACT -->
## Contact

Rodrigo Andaya Jr - rodrigoandayajr.cs@gmail.com  
John Paul Feliciano - johnpaulfeliciano98@gmail.com

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [Regular Expression Operations](https://docs.python.org/3/library/re.html)
* [Pandas](https://pandas.pydata.org/docs/)
* [Scourgify](https://github.com/GreenBuildingRegistry/usaddress-scourgify)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
[contributors-shield]: https://img.shields.io/github/contributors/othneildrew/Best-README-Template.svg?style=for-the-badge
[contributors-url]: https://github.com/rjandaya/vpambu-ctc-report-generator/graphs/contributors
[stars-shield]: https://img.shields.io/github/stars/rjandaya/vpambu-ctc-report-generator?style=for-the-badge
[stars-url]: https://github.com/rjandaya/vpambu-ctc-report-generator/stargazers
[license-shield]: https://img.shields.io/github/license/rjandaya/vpambu-ctc-report-generator?style=for-the-badge
[license-url]: https://github.com/rjandaya/vpambu-ctc-report-generator/blob/main/LICENSE
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/rodrigoandayajr/
[linkedin-shield1]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url1]: https://www.linkedin.com/in/johnp-feliciano/
[Python-url]: https://www.python.org/
[Python]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54
