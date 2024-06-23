from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.transcribe import transcribe_audio
from app.summarize import summarize_text
from app.timestamps import extract_timestamps
import aiofiles
import os

app = FastAPI()

# Setting up the templates directory
templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
async def get_form(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})

@app.post("/process-audio/")
async def process_audio(file: UploadFile = File(...)):
    try:
        # Ensure the temp_files directory exists
        os.makedirs('temp_files', exist_ok=True)

        # Save the uploaded file locally
        file_location = f"temp_files/{file.filename}"
        async with aiofiles.open(file_location, 'wb') as out_file:
            content = await file.read()
            await out_file.write(content)

        # Transcribe the audio file
        transcription = transcribe_audio(file_location)
        
        # Summarize the transcribed text
        summary = summarize_text(transcription)
        
        # Extract timestamps from the transcription
        timestamps = extract_timestamps(transcription)

        # Save the results locally
        result_location = f"temp_files/{file.filename}.json"
        async with aiofiles.open(result_location, 'w') as out_file:
            results = {
                "transcription": transcription,
                "summary": summary,
                "timestamps": timestamps
            }
            await out_file.write(str(results))

        # Prepare the response
        response = {
            "message": "Processing complete. Results saved locally.",
            "file": result_location
        }

        return JSONResponse(content=response)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


  
