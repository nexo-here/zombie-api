from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from PIL import Image, ImageEnhance
import io

app = FastAPI()

@app.post("/zombify")
async def zombify(image: UploadFile = File(...)):
    # ছবিটা পিল-এ খুলো
    img = Image.open(image.file).convert("RGB")

    # ফ্ল্যাট ফিল্টার: saturation কমাও, contrast বাড়াও
    enhancer = ImageEnhance.Color(img)
    img = enhancer.enhance(0.1)  # desaturate

    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.5)  # increase contrast

    enhancer = ImageEnhance.Brightness(img)
    img = enhancer.enhance(0.7)  # darken

    # Blur একটু দিলে zombie টাইপ লাগে
    img = img.filter(Image.BLUR)

    # সেভ করো
    output = io.BytesIO()
    img.save(output, format="PNG")
    output.seek(0)

    return FileResponse(output, media_type="image/png", filename="zombified.png")
  
