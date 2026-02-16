# Google Cloud Vision API Key Setup Guide

This document explains how to generate and configure a Google Cloud Vision API key for use with the Handwriting OCR MCP server.

## 1. Create a Google Cloud Project

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Click the project selection dropdown in the top navigation bar.
3. Click **New Project**.
4. Enter a project name and click **Create**.

## 2. Link a Billing Account (Required)

To use the Google Cloud Vision API, a billing account must be linked. (Usage is available within the free tier)

1. Go to **Billing** in the left menu.
2. Click **Link a billing account** and follow the instructions to register your billing information.

## 3. Enable Vision API

1. Enter "Cloud Vision API" in the top search bar and select it.
2. Click the **Enable** button to activate the API.


## 4. Create Service Account Key

1. Go to **APIs & Services** > **Credentials** in the left menu.
2. Click **+ Create Credentials** at the top and select **Service Account**.
3. Enter service account details and click **Create and Continue**.
4. (Optional) In the role selection step, grant an appropriate role such as **Cloud Vision API User**.
5. Click **Done** to create the service account.
6. Click the created service account and go to the **Keys** tab.
7. Click **Add Key** > **Create new key** and select **JSON**.
8. Save the downloaded JSON file to a secure location. (e.g., outside the project root or in a path added to `.gitignore`)

## 5. Project Configuration

Enter the path of the issued key file in the `.env` file in the project root directory.

1. Create a `.env` file by copying the `.env.example` file. (Skip if it already exists)
   ```bash
   cp .env.example .env
   ```
2. Open the `.env` file and enter the **absolute path** of the JSON key file in the `GOOGLE_APPLICATION_CREDENTIALS` field.
   ```
   GOOGLE_APPLICATION_CREDENTIALS="/Users/username/keys/my-project-key.json"
   ```

## 6. Verification

To verify that the configuration is correct, you can restart the MCP server or use the test feature of the installation script.

If the API key is invalid or the quota is exceeded, the server will automatically switch to Tesseract OCR (if installed) to operate.
