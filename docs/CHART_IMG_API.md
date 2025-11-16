# Chart-IMG API Key Configuration

The Legend AI dashboard uses the Chart-IMG API to generate and display trading charts. To use this feature, you need to obtain a free API key from Chart-IMG and configure it as an environment variable in your Railway deployment.

## Obtaining a Chart-IMG API Key

1.  **Sign up for a free account:** Go to the [Chart-IMG website](https://chart-img.com/) and sign up for a free account.
2.  **Get your API key:** Once you've signed up, you'll find your API key in your account dashboard.

## Configuring the API Key in Railway

1.  **Open your Railway project:** Go to your Legend AI project in the Railway dashboard.
2.  **Go to the "Variables" tab:** In your project settings, you'll find a "Variables" tab.
3.  **Add a new variable:** Click on the "New Variable" button and add a new variable with the following details:
    *   **Name:** `CHARTIMG_API_KEY`
    *   **Value:** Paste your Chart-IMG API key here.
4.  **Redeploy your application:** After adding the new variable, Railway will automatically redeploy your application.

Once your application has been redeployed, the charts should load correctly in the dashboard.
