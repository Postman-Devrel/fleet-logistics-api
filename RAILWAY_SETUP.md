# Railway Deployment Guide

## Step-by-Step Setup

### 1. Create Railway Project
1. Go to https://railway.app
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose your `fleet-logistics-api` repository
5. Railway will start building and deploying

### 2. Add PostgreSQL Database
**IMPORTANT:** This step is required for the app to work!

1. In your Railway project dashboard, click "New" button
2. Select "Database"
3. Choose "Add PostgreSQL"
4. Railway will provision a new Postgres database
5. **The `DATABASE_URL` environment variable will be automatically added to your service**

### 3. Verify Environment Variables
1. Click on your web service (not the database)
2. Go to the "Variables" tab
3. You should see `DATABASE_URL` listed
4. If not, you need to link the database:
   - Click "New Variable"
   - Click "Add Reference"
   - Select your PostgreSQL database
   - Choose `DATABASE_URL`

### 4. Verify Deployment
1. Click on your web service
2. Go to "Deployments" tab
3. Wait for the latest deployment to complete
4. Click on the generated URL (e.g., `https://your-app.railway.app`)
5. You should see: `{"message": "Fleet Logistics API", ...}`

### 5. Check Health Status
Visit: `https://your-app.railway.app/health`

You should see:
```json
{
  "status": "healthy",
  "database": "connected",
  "database_url_configured": true
}
```

If you see:
- `"database": "error: ..."` - Database connection failed
- `"database_url_configured": false` - DATABASE_URL not set

### 6. Seed the Database
Once the app is running and database is connected:

**Option A: Using Railway CLI**
```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Link to your project
railway link

# Run seed script
railway run python scripts/seed_data.py
```

**Option B: Using Local Script with Remote DB**
```bash
# Get DATABASE_URL from Railway dashboard
# Copy it from Variables tab

# Set it locally
export DATABASE_URL="postgresql://postgres:..."

# Run seed script
python scripts/seed_data.py
```

**Option C: Using Railway Shell**
1. In Railway dashboard, click on your service
2. Click "Shell" tab (in the top menu)
3. Wait for shell to connect
4. Run: `python scripts/seed_data.py`

## Troubleshooting

### App Crashes Immediately
**Check:** Did you add PostgreSQL database?
- Go to Railway project
- Click "New" → "Database" → "Add PostgreSQL"

### Database Shows "error: connection refused"
**Check:** Is DATABASE_URL set correctly?
- Go to your service → Variables tab
- Verify `DATABASE_URL` exists
- It should start with `postgresql://`

### DATABASE_URL Not Showing
**Fix:** Add database reference manually
1. Click your web service
2. Go to Variables tab
3. Click "New Variable" → "Add Reference"
4. Select PostgreSQL database → `DATABASE_URL`
5. Redeploy

### Deployment Succeeds but App Shows Errors
**Check:** Visit `/health` endpoint
```bash
curl https://your-app.railway.app/health
```

Look at the response to diagnose the issue.

### Need to See Logs
1. Click on your service in Railway
2. Go to "Deployments" tab
3. Click on the latest deployment
4. View the logs to see what's happening

## Common Railway Environment Variables

Railway automatically provides:
- `DATABASE_URL` - PostgreSQL connection string (when database is added)
- `PORT` - Port your app should listen on
- `RAILWAY_ENVIRONMENT` - Environment name (production/staging)

## After Successful Deployment

1. Visit your API docs: `https://your-app.railway.app/docs`
2. Import to Postman: `https://your-app.railway.app/openapi.json`
3. Start testing!

## Manual Environment Variable Setup (if needed)

If DATABASE_URL is not automatically set:

1. Go to Railway project → PostgreSQL database
2. Click "Variables" tab
3. Copy the `DATABASE_URL` value
4. Go to your web service → Variables tab
5. Click "New Variable"
6. Name: `DATABASE_URL`
7. Value: paste the copied value
8. Deploy

## Checking Database Connection Locally

Test your Railway database from local machine:
```bash
# Get DATABASE_URL from Railway
export DATABASE_URL="your-railway-postgres-url"

# Test with psql
psql $DATABASE_URL

# Or test with Python
python -c "from app.database.config import engine; engine.connect(); print('Connected!')"
```
