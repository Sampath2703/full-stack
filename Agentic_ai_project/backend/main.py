from fastapi import FastAPI, Request
from database import supabase
from agents.orchestrator import orchestrate

app = FastAPI()


@app.post("/login")
async def login(request: Request):

    payload = await request.json()

    Email = payload.get("Email")
    Password = payload.get("Password")

    res = supabase.table("register") \
        .select("*") \
        .eq("Email", Email) \
        .eq("Password", Password) \
        .execute()

    if not res.data:
        supabase.table("logs").insert({
            "user_email": Email,
            "event": "LOGIN_FAILED",
            "source_ip": "127.0.0.1",
            "log_data": "Invalid login",
            "log_type": "AUTH",
            "severity": "MEDIUM",
            "is_threat": True
        }).execute()

        return {"status": "error", "message": "Invalid credentials"}

    user = res.data[0]

    supabase.table("logs").insert({
        "user_email": Email,
        "event": "LOGIN_SUCCESS",
        "source_ip": "127.0.0.1",
        "log_data": "User logged in",
        "log_type": "AUTH",
        "severity": "LOW",
        "is_threat": False
    }).execute()

    return {"status": "success", "user": user}


@app.get("/logs")
async def get_logs():
    res = supabase.table("logs").select("*").execute()
    return {"status": "success", "data": res.data}


@app.get("/run_pipeline")
async def run_pipeline():
    res = supabase.table("logs").select("*").execute()
    logs = res.data

    result = orchestrate(logs)

    return {"status": "success", "data": result}