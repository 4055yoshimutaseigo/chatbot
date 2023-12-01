from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
import openai

from .models import Message


def index(request): # 最初の画面、過去のMessage.objects(履歴)をhtmlに表示する
    messages = Message.objects.order_by('-created_at').reverse() # クエリセット（モデルのデータベースから取り出したデータ）を降順に並び替えて取得し変数へ代入
    context = {'messages': messages} # 辞書型へ
    return render(request, 'chat/index.html', context) # return render(大抵request,表示させたいHTML,渡したい変数)


def post(request): # htmlのfromが入力されると、内容がpost関数へやってくる

    if request.method == "POST":
        # タイトル下のテキストボックス（出発地は？目的地は？何泊しますか？）
        if "departure" in request.POST:
            departure = request.POST['departure']
            destination = request.POST['destination']
            stay = request.POST['stay']
            question = f"{departure}から{destination}の、{stay}の旅行プランを提案してください。初めの５文字だけ返答してください"
        # 画面下のフリー入力フォーム
        if "contents" in request.POST:
            contents = request.POST['contents']
            question = f"{contents}。初めの５文字だけ返答してください"
        # ボタン
        elif "tourist_spot" in request.POST:
            question = "観光地についてもっと詳しく教えてください。初めの５文字だけ返答してください"
        elif "hotel" in request.POST:
            question = "ホテルについてもっと詳しく教えてください。初めの５文字だけ返答してください"
        elif "gourmet" in request.POST:
            question = "グルメやおいしいレストランについてもっと詳しく教えてください。初めの５文字だけ返答してください"
        elif "souvenir" in request.POST:
            question = "お土産についてもっと詳しく教えてください。初めの５文字だけ返答してください"
        elif "reset" in request.POST:
            question = "今までの会話をリセットしてください"


    openai.api_key = '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'
# chatGPTからのレスポンスを代入
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "日本語で応答してください" # 事前に細かい指示を入れる
            },
            {
                "role": "user", # ユーザーからの質問という意味
                "content": question # chatGPTへの質問
            },
        ]
    )

# chatGPTからのレスポンス(辞書型)の中から必要なものを抜き出す
    results = response["choices"][0]["message"]["content"]

# モデルからオブジェクトを１つ作成し、データベースに保存
    Message.objects.create(
        contents=question, # ユーザーの質問
        response=results, # ChatGPTの返事
        created_at=timezone.now()
    )
    return redirect('chat:index') # index関数にリダイレクト

