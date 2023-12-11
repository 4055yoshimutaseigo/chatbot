from django.shortcuts import render, redirect
from django.utils import timezone
import openai
import random
from datetime import datetime
from .models import Message, Answer


def index(request): # 最初の画面、過去のMessage.objects(履歴)をhtmlに表示する
    messages = Message.objects.order_by('-created_at').reverse() # クエリセット（モデルのデータベースから取り出したデータ）を降順に並び替えて取得し変数へ代入
    context = {'messages': messages} # 辞書型へ

    # 朝、昼、夕方、夜に応じて背景を変更
    now = datetime.now()  # 現在時刻の取得
    hour = now.hour
    if 5 <= hour < 12:
        background_image = 'mountain08.png'
    elif 12 <= hour < 18:
        background_image = 'beach10.png'
    elif 18 <= hour < 22:
        background_image = 'hill_evening05.png'
    else:
        background_image = 'milkyway01.png'

    # 11行目で作成したcontext(辞書型)に結合
    context['background_image'] = f'../static/images/{background_image}'

    return render(request, 'chat/index.html', context) # return render(大抵request,表示させたいHTML,渡したい変数)


def post(request): # htmlのfromが入力されると、内容がpost関数へやってくる

    if request.method == "POST":
        if "departure" in request.POST:
            departure = request.POST['departure']
            destination = request.POST['destination']
            stay = request.POST['stay']
            question = f"{departure}から{destination}の、{stay}の旅行プランを提案してください。"

            Answer.objects.create(
                departure=departure,
                destination=destination,
                stay=stay,
                created_at=timezone.now()
                )


        # 画面下のフリー入力フォーム
        elif "contents" in request.POST:
            contents = request.POST['contents']
            question = f"{contents}。"


        # ボタン
        elif "tourist_spot" in request.POST:
            last_answer=Answer.objects.order_by('created_at').last() # 最新のデータベースを取得
            question = f"{last_answer.destination}の観光地についてもっと詳しく教えてください。"

        elif "hotel" in request.POST:
            last_answer = Answer.objects.order_by('created_at').last()  # 最新のデータベースを取得
            question = f"{last_answer.destination}のホテルについてもっと詳しく教えてください。"

        elif "gourmet" in request.POST:
            last_answer = Answer.objects.order_by('created_at').last()  # 最新のデータベースを取得
            question = f"{last_answer.destination}のグルメやおいしいレストランについてもっと詳しく教えてください。"

        elif "souvenir" in request.POST:
            last_answer = Answer.objects.order_by('created_at').last()  # 最新のデータベースを取得
            question = f"{last_answer.destination}のお土産についてもっと詳しく教えてください。"

        elif "reset" in request.POST:
            question = "今までの会話をリセットしてください。"


    openai.api_key = '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'
# chatGPTからのレスポンスを代入
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "日本語で応答してください。あなたは旅行のモデルプランを作成するプランナーです。質問されたことに対して、「さらに詳しく詳細な情報が必要です」という旨の返答をしないでください。もし、今までの会話をリセットしてくださいと言われたら、「今までの会話をリセットしました。タイトル下のフォームに新しい行先を入力してください」と返答してください。" # 事前に細かい指示を入れる
            },
            {
                "role": "user", # ユーザーからの質問
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


def lottery(request):
    destination_lottery = {"destination1": ""}  # 初期値を設定
    if request.method == "POST":
        if "travel_lottery" in request.POST:
            lottery_list = ["北海道", "草津温泉", "シンガポール", "名古屋"]
            a = random.choice(lottery_list)
            b = f"{a}がおすすめ"
            destination_lottery = {"destination1" : b}
    return render(request, "chat/lottery.html", destination_lottery)
