import os, json
from datetime import datetime, timedelta
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from passlib.context import CryptContext
from jose import jwt

app = FastAPI()
SECRET_KEY = "pocketsmart123"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
USERS_FILE = "users.json"

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f: return json.load(f)
    return {}
def save_users(u):
    with open(USERS_FILE, "w") as f: json.dump(u, f, indent=2)
def get_hash(p): return pwd_context.hash(str(p)[:72])
def verify(p, h): return pwd_context.verify(str(p)[:72], h)
def create_token(d):
    d["exp"] = datetime.utcnow() + timedelta(hours=5)
    return jwt.encode(d, SECRET_KEY, algorithm="HS256")
def get_user(req: Request):
    t = req.cookies.get("access_token")
    if not t: return None
    try:
        payload = jwt.decode(t.replace("Bearer ",""), SECRET_KEY, algorithms=["HS256"])
        return load_users().get(payload.get("sub"))
    except: return None

STYLE = "body{font-family:Arial;padding:20px}.card{border:1px solid #eee;padding:20px;border-radius:15px;max-width:600px;margin:20px auto} input,select{width:100%;padding:10px;margin:8px 0} button{width:100%;padding:12px;background:#6c5ce7;color:white;border:none;border-radius:8px;font-size:16px}.btn{padding:12px 20px;color:white;border-radius:10px;text-decoration:none;display:inline-block;margin:5px}"

@app.get("/", response_class=HTMLResponse)
async def home():
    return f"""<html><head><style>{STYLE}</style></head><body style="text-align:center">
    <h1>PocketSmart AI</h1><p>Onna select pannu da</p>
    <div><a href='/home-planner' style='{STYLE}' class='btn' style='background:#6c5ce7'>🏠 Home Planner</a>
    <a href='/party-planner' class='btn' style='background:#00b894'>🎉 Party Planner</a>
    <a href='/jewelry-planner' class='btn' style='background:#e84393'>💍 Jewelry Planner</a></div>
    </body></html>"""

@app.get("/register", response_class=HTMLResponse)
async def reg(): return """<html><body style="display:flex;justify-content:center;padding:50px;font-family:Arial"><div style="border:1px solid #ddd;padding:30px;border-radius:15px;width:320px">
    <h2>Create Account</h2><form method="post" action="/register">
    <input name="username" placeholder="Username" required style="width:100%;padding:10px;margin:8px 0"><br>
    <input name="email" type="email" placeholder="Email" required style="width:100%;padding:10px;margin:8px 0"><br>
    <input name="password" type="password" placeholder="Password" required style="width:100%;padding:10px;margin:8px 0"><br>
    <button style="width:100%;padding:12px;background:#6c5ce7;color:white;border:none;border-radius:8px">Create Account</button></form></div></body></html>"""

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    u = get_user(request)
    if not u: return RedirectResponse("/register", status_code=302)
    return await home()

# --- 3 DIFFERENT PLANNERS ---
@app.get("/home-planner", response_class=HTMLResponse)
async def hp(req: Request):
    u = get_user(req)
    if not u: return RedirectResponse("/register?next=/home-planner", status_code=302)
    return f"""<html><head><style>{STYLE}</style></head><body><div class="card">
    <h2>🏠 Home Interior Planner - Hi {u['username']}</h2>
    <label>Total Budget</label><input id="b" type="number" value="50000">
    <label>Room Type</label><select id="r"><option>Living Room</option><option>Bedroom</option><option>Kitchen</option></select>
    <button onclick="genHome()">Generate Home Plan</button>
    <pre id="res" style="background:#f5f5f5;padding:15px;margin-top:15px;white-space:pre-wrap"></pre>
    <a href="/">Back</a></div>
    <script>
    function genHome(){{
        let b=document.getElementById('b').value; let r=document.getElementById('r').value;
        document.getElementById('res').innerText = `HOME PLAN for ${{r}} - Rs.${{b}}\\n----------------\\n- IKEA Sofa Set: Rs.${{b*0.4}}\\n- Amazon Lights: Rs.${{b*0.2}}\\n- Flipkart Furniture: Rs.${{b*0.4}}\\n\\nTip: Add Gemini API for real AI!`;
    }}
    </script></body></html>"""

@app.get("/party-planner", response_class=HTMLResponse)
async def pp(req: Request):
    u = get_user(req)
    if not u: return RedirectResponse("/register?next=/party-planner", status_code=302)
    return f"""<html><head><style>{STYLE}</style></head><body><div class="card">
    <h2>🎉 Party Planner - Hi {u['username']}</h2>
    <label>Total Budget</label><input id="b" type="number" value="30000">
    <label>Guest Count</label><input id="g" type="number" value="50">
    <label>Event Type</label><select id="e"><option>Birthday</option><option>Wedding</option><option>House Warming</option></select>
    <button onclick="genParty()">Generate Party Plan</button>
    <pre id="res" style="background:#f5f5f5;padding:15px;margin-top:15px;white-space:pre-wrap"></pre>
    <a href="/">Back</a></div>
    <script>
    function genParty(){{
        let b=document.getElementById('b').value; let g=document.getElementById('g').value; let e=document.getElementById('e').value;
        document.getElementById('res').innerText = `PARTY PLAN for ${{e}} - Rs.${{b}} / ${{g}} Guests\\n----------------\\n- Venue/Decoration: Rs.${{b*0.5}}\\n- Food & Cake: Rs.${{b*0.3}}\\n- Music & Lights: Rs.${{b*0.2}}\\nPer person: Rs.${{b/g}}\\n`;
    }}
    </script></body></html>"""

@app.get("/jewelry-planner", response_class=HTMLResponse)
async def jp(req: Request):
    u = get_user(req)
    if not u: return RedirectResponse("/register?next=/jewelry-planner", status_code=302)
    return f"""<html><head><style>{STYLE}</style></head><body><div class="card">
    <h2>💍 Jewelry Planner - Hi {u['username']}</h2>
    <label>Total Budget</label><input id="b" type="number" value="100000">
    <label>Occasion</label><select id="o"><option>Wedding</option><option>Festival</option><option>Daily Wear</option></select>
    <label>Style</label><select id="s"><option>Gold</option><option>Diamond</option><option>Silver</option></select>
    <button onclick="genJew()">Generate Jewelry Plan</button>
    <pre id="res" style="background:#f5f5f5;padding:15px;margin-top:15px;white-space:pre-wrap"></pre>
    <a href="/">Back</a></div>
    <script>
    function genJew(){{
        let b=document.getElementById('b').value; let o=document.getElementById('o').value; let s=document.getElementById('s').value;
        document.getElementById('res').innerText = `JEWELRY PLAN for ${{o}} - ${{s}} - Rs.${{b}}\\n----------------\\n- Necklace (${{s}}): Rs.${{b*0.5}}\\n- Earrings: Rs.${{b*0.3}}\\n- Bangles/Ring: Rs.${{b*0.2}}\\n`;
    }}
    </script></body></html>"""

@app.post("/register")
async def register(username: str = Form(...), email: str = Form(...), password: str = Form(...)):
    users = load_users()
    users[username] = {"username": username, "email": email, "hashed_password": get_hash(password)}
    save_users(users)
    token = create_token({"sub": username})
    r = RedirectResponse("/", status_code=302)
    r.set_cookie(key="access_token", value=f"Bearer {token}", httponly=True)
    return r
import uvicorn

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)