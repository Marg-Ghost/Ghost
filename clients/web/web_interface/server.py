from fastapi import FastAPI, HTTPException, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID, uuid4
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os
from pathlib import Path
#my
from GetSystemInfo import Dashboard, Folder

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory="web"), name="static")
Dashboard_ = Dashboard()


###################################
##main page
###################################
@app.get("/")
async def load_surface():
	try:
		file_path = Path("web/index.html")
		Dashboard_.get_all_data()
		return FileResponse(str(file_path))
	except Exception as e:
		raise HTTPException(status_code=404, detail="index.html")

@app.api_route("/dashboard", methods=["GET","POST"])
async def get_dashboard():
    return Dashboard_.get_all_data()

@app.get("/dashboard/src")
async def dashboard_src(payload: dict):
	try:
		section = payload.get("section", "src")
		folder = Folder(section)
		return folder.prew()
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

##################################
##Eignen Ordner
####################################
# src folder
@app.get("/src")
async def load_src():
	try:
		folder = Folder("src")
		return folder.show_whole_dir()
	except Exception as e:
		raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=4200)
