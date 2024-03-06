# photo-to-icon
Dockerを用いてコンテナ上で開発しました。
photo-to-iconディレクトリにNext.jsのソースコードが、Pythonディレクトリにmain.pyのソースコードが配置されています。  
PythonではFastAPIを用いてバックエンドのAPI開発をしました。
ユーザーがjpeg、png形式の画像をアップロードすると、OpenAIのGPT4-VisionのAPIにDall-E3で画像生成するためのプロンプトを生成してもらい、
そのプロンプトをDall-E3のAPIに投げることで、アイコン画像を生成しています。

# 動作している様子
![](dousa.png)