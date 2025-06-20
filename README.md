# Lead Generator Pro

Lead Generator Pro is a powerful, web-based application designed to automate the process of finding and qualifying business leads from Google Maps. It features a deep-scraping engine that not only gathers basic business information but also crawls company websites to find contact details, social media profiles, and key employee information.

The entire application is managed through a user-friendly Flask web interface, providing real-time progress updates and easy-to-download results.

## Key Features

- **Interactive Web Interface:** A clean, modern UI built with Flask and JavaScript for easy operation. No command-line interaction needed.
- **Deep Website Crawling:** Intelligently navigates from a business's homepage to its "Contact," "About," or "Team" pages to find more data.
- **Comprehensive Data Extraction:**
    - **Business Info:** Name, Rating, Review Count, Category, Address, Phone, Website.
    - **Contact Info:** Gathers all unique emails found across the website.
    - **Social Media:** Finds company pages on LinkedIn, Facebook, Instagram, and Twitter.
    - **Employee Details:** Extracts employee names, job titles, and contact info (email, LinkedIn) from team pages.
- **LinkedIn Integration:** Logs into a provided LinkedIn account to scrape details from employee profiles, enriching the lead data.
- **Real-Time Progress:** The UI shows live status messages and a progress bar during scraping.
- **Downloadable Results:** Easily download the final lead list in both **CSV** and **JSON** formats.
- **Secure Credential Handling:** Uses a local `config.json` file for LinkedIn credentials, which is never committed to version control thanks to a robust `.gitignore`.

## Technology Stack

- **Backend:** Python, Flask
- **Frontend:** HTML, CSS, JavaScript (no frameworks)
- **Scraping Engine:** Selenium

## Setup and Installation

Follow these steps to get the application running on your local machine.

### 1. Prerequisites

- Python 3.8+
- Google Chrome browser

### 2. Clone the Repository

```bash
git clone https://github.com/toobajatoi/lead-gen.git
cd lead-gen
```

### 3. Install Dependencies

It's recommended to use a virtual environment.

```bash
# Create and activate a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

# Install required Python packages
pip install -r requirements.txt
```

### 4. Configure LinkedIn Credentials (Required for Employee Scraping)

To unlock the powerful LinkedIn employee scraping feature, you must provide credentials.

1.  Find the `config.json.example` file in the project directory.
2.  **Rename or copy** it to a new file named `config.json`.
3.  Open `config.json` and replace the placeholder values with your actual LinkedIn email and password.

```json
{
    "linkedin_email": "your-email@example.com",
    "linkedin_password": "your-linkedin-password"
}
```
**Note:** Your `config.json` file is listed in `.gitignore` and will never be pushed to GitHub.

## How to Run the Application

1.  Make sure you are in the project's root directory and your virtual environment (if any) is activated.
2.  Start the Flask server:

    ```bash
    python app.py
    ```
3.  Open your web browser and navigate to:

    [http://localhost:5000](http://localhost:5000)

## How to Use the Web Interface

1.  **Enter a Search Query:** Type your desired search into the input field (e.g., `restaurants in new york`, `software companies in san francisco`).
2.  **Set Target Number of Leads:** Choose how many businesses you want to find.
3.  **Start Scraping:** Click the "Start Scraping" button.
4.  **Monitor Progress:** Watch the progress bar and status messages for live updates. The browser window managed by Selenium will appear and perform the scraping tasks.
5.  **Download Results:** Once the scraping is complete, the results will appear in a table. Use the "Download CSV" or "Download JSON" buttons to save your lead list. 