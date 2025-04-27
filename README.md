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

2. Generate HTTPS certificate:
   ```bash
   certbot certonly --standalone -d <YOUR_DOMAIN>
   ```

3. Configure environment:
   ```bash
   cp .env.example .env
   # Fill in the credentials from step 1
   ```

4. Start service:

   ```bash
   docker-compose up -d
   ```

5. Visit `https://<YOUR_DOMAIN>/api/oauth/start` to install the agent to your Linear workspace

After installation, you can @mention and assign issues to this agent in Linear.

## Environment Variables (`.env`)

```env
LINEAR_CLIENT_ID=      # OAuth Client ID
LINEAR_CLIENT_SECRET=  # OAuth Client Secret  
LINEAR_WEBHOOK_SECRET= # Webhook Signing Secret
BASE_URL=             # https://<YOUR_DOMAIN>
```