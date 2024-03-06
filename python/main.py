from fastapi import FastAPI, UploadFile
import shutil
import base64
from openai import OpenAI
from dotenv import load_dotenv
import os
import uuid
from starlette.middleware.cors import CORSMiddleware


# 画像をbase64で読み込む関数
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,   # 追記により追加
    allow_methods=["*"],      # 追記により追加
    allow_headers=["*"]       # 追記により追加
)

@app.get("/")
def read_root():
    return {"message": "root"}


@app.post("/upload")
def get_icon(upload_file: UploadFile):
    # 指定したパスにアップされた画像を保存
    path = f"files/{upload_file.filename}"
    with open(path, "+wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)
    # 画像のファイル名を名前と拡張子に分けて、名前をuuidに変え、元の拡張子と結合
    # ファイル名の重複を防ぐため
    filename_without_extension, extension = os.path.splitext(upload_file.filename)
    new_filename = str(uuid.uuid4()) + extension
    new_path = f"files/{new_filename}"
    shutil.move(path, new_path)
    
    base64_image = encode_image(new_path)

    client = OpenAI(api_key=os.environ["API_KEY"])

    response_gpt4 = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "I want to create an avatar of the person in this photo in 8-bit style. Please capture facial features in detail, and I would like you to create a prompt for me to generate in DALL-E 3. However, please output only the prompt.",
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}",
                        },
                    },
                ],
            }
        ],
        max_tokens=300,
    )

    print("GPTのレスポンス:" + response_gpt4.choices[0].message.content)

    dalle_prompt = (
        response_gpt4.choices[0].message.content + " and flat design, one person, japanese"
    )
    print("dalleに投げるプロンプト:" + dalle_prompt)

    response_dalle = client.images.generate(
        model="dall-e-3",
        prompt=dalle_prompt,
        # prompt="Create an 8-bit style avatar of a person with a friendly smile, wearing a black jacket over a light-colored shirt, and making a peace sign with one hand. His hairstyle is a bowl cut. He has small eyes. The background should be a solid color. flat design. one person.",
        size="1024x1024",
        quality="standard",
        n=1,
    )

    print("生成された画像のurl: " + response_dalle.data[0].url)

    return {"upload_filename": upload_file.filename, "type": upload_file.content_type, "revised_prompt": response_dalle.data[0].revised_prompt, "image_url": response_dalle.data[0].url}
