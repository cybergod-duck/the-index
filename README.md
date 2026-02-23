# CRM Index: Autonomous SEO & Automation Matrix

This repository contains the architecture, build scripts, and autonomous syndication bots that power **CRM Index**, a programmatic SEO platform generating hyper-niche B2B pages designed to funnel organic traffic to high-tier software affiliates.

## Project Structure

*   **/public**: Contains the pre-rendered, static HTML for the CRM industry pages, as well as the generated XML sitemap.
*   **`build.py`**: The dynamic Python site generator. It ingests `data.csv`, parses the industry constraints, injects the favicons and tracking, generates targeted HTML slug pages, and outputs `sitemap.xml`.
*   **`data.csv`**: The master database containing industries, pain points, and URLs for all potential SEO pages.

## The Titan Automation Suite

To guarantee the site is indexed rapidly and builds massive domain authority, four independent "Titan" agents run on a daily scheduled loop to syndicate the CRM pages across the web's highest Authority platforms.

1.  **X Titan (`x_api_titan.py`)**: 
    Connected directly to the official X API via Tweepy. Organically drops a conversational tweet with the appropriate CRM link to build social signals.
2.  **LinkedIn Titan (`linkedin_titan.py`)**: 
    Automates an anti-detect Chrome profile to craft professional B2B posts on LinkedIn. It waits for the meta-preview card to render before publishing to ensure high-conversion visual appeal.
3.  **Reddit AEO Titan (`reddit_titan.py`)**: 
    An "Answer Engine Optimization" Trojan Horse. It actively searches Reddit for B2B threads discussing business systems/invoicing, reads the context, and injects a conversational, typo-laden suggestion to use a specific CRM Index page, bypassing AI detection.
4.  **Pinterest Titan (`solo_titan.py`)**: 
    A massive bulk visual-pinning engine. It autonomously posts beautifully styled, high-converting pins to Pinterest Boards. When it runs low on assets, it auto-triggers `premium_pin_generator.py` to batch-render 150 new graphic designs in the background via HTML-to-Image.

## Setup & Execution

### Prerequisites
* Python 3.12+
* Google Chrome

```bash
pip install selenium rich webdriver-manager tweepy html2image
```

### Running the Build
```bash
python build.py
```
This reads the `data.csv` and compiles the web architecture into the `/public` folder, generating the `sitemap.xml`.

### Running the Bots
The bots are designed to be run via Windows Task Scheduler to guarantee a steady drip of backlinks. They require the authenticated `chrome_profile_final` directory to maintain stateless sessions safely.

### State Tracking
Each bot maintains its own lightweight JSON state database (e.g., `x_api_state.json`, `linkedin_state.json`) to keep track of URLs it has already posted, ensuring all bots distribute links evenly without duplicating their individual posts.
