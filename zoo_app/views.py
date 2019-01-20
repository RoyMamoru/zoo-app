from django.shortcuts import render, redirect
# 画像ファイルUploadで使用
from django.conf import settings
from django.core.files.storage import FileSystemStorage
# 推論用のモジュール
import numpy as np
import cv2
import chainer
import chainer.links as L
import chainer.functions as F
from chainer.links.model.vision.googlenet import prepare
from .trained_model.trained_model import GoogleNetModel
# DBのインポート
from .models import ZooCollection, AnimalInfo
import csv
# ログイン認証
from django.contrib.auth.decorators import login_required
# サインアップ
from .forms import SignUpForm
from django.contrib.auth import login, authenticate

# モデルの読み込みとラベルの定義
model = L.Classifier(GoogleNetModel())
chainer.serializers.load_npz('zoo_app/trained_model/model_gnet_finetune.npz', model)

# DB内にデータがない場合に動物データを登録したDBの作成
animalsinfo = list(AnimalInfo.objects.all())
if not animalsinfo:
    with open('zoo_app/static/data/animal_data.csv', 'r') as f:
        data = csv.reader(f)
        data = [row for row in data]
    for i, _data in enumerate(data[1:]):
        ani_name, ani_title, ani_disc = _data
        aniinfo = AnimalInfo(animal_id=i, animal_name=ani_name, animal_title=ani_title, animal_disc=ani_disc)
        aniinfo.save()

@login_required
def classify(request):
    if request.method == 'POST' and request.FILES['predict_img']:
        predict_img = request.FILES['predict_img']
        fs = FileSystemStorage()
        filename = fs.save(predict_img.name, predict_img)
        uploaded_file_url = fs.url(filename)

        # 推論処理
        img = cv2.cvtColor(cv2.imread('media/{}'.format(filename)), cv2.COLOR_BGR2RGB)
        x = prepare(img)
        y = model.predictor(np.array([x]))
        y_proba = F.softmax(y).data
        y_pre = np.argmax(y_proba, axis=1)[0]
        proba = round(y_proba[0][y_pre] * 100, 2)

        # AnimalInfoのDBから必要な情報の取得
        animal_info = AnimalInfo.objects.filter(animal_id=y_pre)

        # ZooCollectionに情報を保存
        current_user = request.user
        if not list(ZooCollection.objects.filter(user_id=current_user.id, animal_id=y_pre)):
            user_info = ZooCollection(user_id=current_user.id, animal_id=y_pre)
            user_info.save()

        return render(request, 'zoo_app/classify.html',{'uploaded_file_url':uploaded_file_url, 'animal_info':animal_info, 'proba':proba})

    return render(request, 'zoo_app/classify.html', {})

@login_required
def history(request):
    current_user = request.user
    collections = ZooCollection.objects.filter(user_id=current_user.id).order_by('animal_id').values_list('animal_id')
    if not collections:
        return render(request, 'zoo_app/history.html', {})
    else:
        historys = []
        for id in collections:
            historys.append(AnimalInfo.objects.filter(animal_id=id[0]))
    return render(request, 'zoo_app/history.html', {'historys':historys})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = SignUpForm()
    return render(request, 'zoo_app/signup.html', {'form': form})
