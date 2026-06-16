from fastapi import FastAPI, Request
from database import supabase
from agents.orchestrator import orchestrate

app = FastAPI()


@app.post("/register")
async def register(request: Request):
    payload = await request.json()

    name = payload.get("Name")
    email = payload.get("Email")
    password = payload.get("Password")

    if not name or not email or not password:
        return {"status": "error"}

    supabase.table("register").insert({
        "Name": name,
        "Email": email,
        "Password": password
    }).execute()

    return {"status": "success"}


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

        return {"status": "error"}

    user = res.data[0]

    supabase.table("logs").insert({
        "user_email": Email,
        "event": "LOGIN_SUCCESS",
        "source_ip": "127.0.0.1",
        "log_data": "Login success",
        "log_type": "AUTH",
        "severity": "LOW",
        "is_threat": False
    }).execute()

    return {"status": "success", "user": user}


@app.get("/run_pipeline")
async def run_pipeline():
    res = supabase.table("logs").select("*").execute()
    logs = res.data

    result = orchestrate(logs)

    return {"status": "success", "data": result}