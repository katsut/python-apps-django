import random

# 名産品データ
meisan = {
    "さくらんぼ": "山形",
    "りんご": "青森",
    "うどん": "香川",
    "もみじ饅頭": "広島",
    "明太子": "福岡",
}

# ゲームの説明
print("=== 全国名産品 都道府県当てクイズ ===")
print("出題された名産品を見て、どの都道府県か答えてね！")
print("（例：りんご → 青森）")

# ランダムに1問出題
item = random.choice(list(meisan.keys()))
print("\n名産品：", item)

# 答えを入力
answer = input("どこの都道府県の名産品でしょう？：")

# 答え合わせ
if answer == meisan[item]:
    print("正解！🎉")
else:
    print("残念！正解は", meisan[item], "です。")
