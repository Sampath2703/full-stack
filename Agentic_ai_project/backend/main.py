from fastapi import FastAPI, Request
from database import supabase
from agents.log_agent import log_agent
from agents.orchestrator import orchestrate
app = FastAPI()


@app.post("/register")
async def register(request: Request):

    payload = await request.json()

    name = payload.get("Name")
    email = payload.get("Email")
    password = payload.get("Password")

    if not name or not email or not password:
        return {"status": "error", "message": "All fields required"}

    existing = supabase.table("register") \
        .select("*") \
        .eq("Email", email) \
        .execute()

    if existing.data:
        return {"status": "error", "message": "User already exists"}

    res = supabase.table("register").insert({
        "Name": name,
        "Email": email,
        "Password": password
    }).execute()

    return {"status": "success", "message": "Registered", "data": res.data}


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
            "log_data": "Invalid login attempt",
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
        "log_data": "User logged in successfully",
        "log_type": "AUTH",
        "severity": "LOW",
        "is_threat": False
    }).execute()

    return {"status": "success", "user": user}


@app.get("/logs")
async def get_logs():

    res = supabase.table("logs").select("*").execute()
    raw_logs = res.data

    processed_logs = log_agent(raw_logs)
    return {"status": "success", "data": res.data}


@app.get("/analyze_logs")
async def analyze_logs():

    res = supabase.table("logs").select("*").execute()
    logs = res.data

    result = []

    for log in logs:

        event = log.get("event", "")

        if event == "LOGIN_SUCCESS":
            log["severity"] = "LOW"
            log["is_threat"] = False

        elif event == "LOGIN_FAILED":
            log["severity"] = "MEDIUM"
            log["is_threat"] = True

        else:
            log["severity"] = "LOW"
            log["is_threat"] = False

        result.append(log)

    return {"status": "success", "data": result}

@app.get("/run_pipeline")
async def run_pipeline():
    res = supabase.table("logs").select("*").execute()
    logs = res.data

    result = orchestrate(logs)

    return{
        "status":"success",
        "data":result
    }