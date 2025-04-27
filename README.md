# Linear Agent Demo

A demo implementation of Linear's agent (app user) that can be mentioned, assigned to issues, and interact with workspace like a regular team member.

## Prerequisites

- A Linear manager account
- A Domain
- A VPS with docker installed

## Setup

1. Create new application at [Linear API Settings](https://linear.app/settings/api/applications/new):
   - Set Callback URL: `https://<YOUR_DOMAIN>/api/oauth/callback`
   - Set Webhook URL: `https://<YOUR_DOMAIN>/webhooks/linear`
   - Enable "Inbox notifications" in webhook settings
   - Save Client ID, Client Secret and Webhook Signing Secret
2. Deploy to Vercel:

   1. Fork this repository
   2. Create a new project on [Vercel](https://vercel.com)
   3. Connect your forked repository
   4. Set up the following environment variables in your Vercel project settings:
      - `LINEAR_CLIENT_ID`: Your Linear OAuth client ID
      - `LINEAR_CLIENT_SECRET`: Your Linear OAuth client secret
      - `LINEAR_WEBHOOK_SECRET`: Your Linear webhook secret
      - `BASE_URL`: Your Vercel deployment URL (e.g., https://your-app.vercel.app)
3. Visit `https://<YOUR_DOMAIN>/api/oauth/start` to install the agent to your Linear workspace
4. Now you can @mention and assign issues to this agent in Linear.

## Environment Variables (`.env`)

```env
LINEAR_CLIENT_ID=      # OAuth Client ID
LINEAR_CLIENT_SECRET=  # OAuth Client Secret  
LINEAR_WEBHOOK_SECRET= # Webhook Signing Secret
BASE_URL=             # https://<YOUR_DOMAIN>
```