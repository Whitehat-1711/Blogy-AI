# Deploy Guide: Vercel + Render

This setup deploys:
- `frontend` on Vercel (React + Vite)
- `Backend` on Render (FastAPI)

## 1) Prepare accounts and secrets

Create these first:
- Render account
- Vercel account
- MongoDB Atlas cluster + connection string
- Groq API key

Keep these values ready:
- `MONGODB_URL`
- `GROQ_API_KEY`

---

## 2) Deploy backend on Render

This repo includes `render.yaml` for the backend service.

1. Push your repo to GitHub.
2. In Render: **New** -> **Blueprint**.
3. Select your repo.
4. Render detects `render.yaml` and proposes `blogy-api`.
5. Continue and create the service.
6. Open the created service -> **Environment** and set:
   - `GROQ_API_KEY` (required)
   - `MONGODB_URL` (required)
   - `CORS_ORIGINS` (temporarily set to `https://your-frontend.vercel.app,http://localhost:5173`)
   - Optional keys if you use them:
     - `SERPAPI_KEY`
     - `HASHNODE_API_TOKEN`
     - `HASHNODE_PUBLICATION_ID`
7. Deploy and wait for status **Live**.
8. Copy backend URL, for example:
   - `https://blogy-api.onrender.com`
9. Verify:
   - Visit `https://blogy-api.onrender.com/health`
   - You should get JSON with `status: "healthy"`.

---

## 3) Deploy frontend on Vercel

1. In Vercel: **Add New...** -> **Project**.
2. Import the same GitHub repo.
3. Set **Root Directory** to `frontend`.
4. Vercel should detect Vite automatically.
5. Add env var:
   - `VITE_API_URL` = your Render backend URL (for example `https://blogy-api.onrender.com`)
6. Deploy.
7. Copy the Vercel URL, for example:
   - `https://your-app.vercel.app`

---

## 4) Final CORS update (important)

After frontend deploy, go back to Render and update:
- `CORS_ORIGINS=https://your-app.vercel.app,http://localhost:5173`

Then redeploy backend (or trigger restart).

---

## 5) Smoke test checklist

1. Open Vercel app URL.
2. Login/signup works.
3. Create a blog and confirm API calls succeed.
4. Check browser network tab:
   - Requests should go to Render URL from `VITE_API_URL`.
5. Check Render logs for backend errors.

---

## 6) Recommended free-tier notes

- Render free web services sleep after inactivity; first request can be slow (cold start).
- MongoDB Atlas free tier is enough for initial usage.
- If latency becomes an issue later, first upgrade Render instance or move to a no-sleep backend.

---

## 7) Optional domain mapping

If you attach custom domains:
- Update `CORS_ORIGINS` with the custom frontend domain.
- Keep local dev origin if needed.
