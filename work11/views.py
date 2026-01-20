from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from dotenv import load_dotenv
import os
import json
import google.generativeai as genai
from .forms import IngredientForm

# Create your views here.


def load_api_key():
    """環境変数からAPIキーを読み込み"""
    load_dotenv()
    return os.getenv("GEMINI_API_KEY")


def call_gemini_api(ingredients, max_retries=1):
    """Gemini APIを呼び出してレシピを生成（リトライ機能付き）"""
    api_key = load_api_key()

    if not api_key or api_key == "your-api-key-here":
        return {
            "error": True,
            "message": "APIキーが設定されていません。.envファイルでGEMINI_API_KEYを設定してください。",
        }

    # プロンプトを作成（JSON形式で）
    ingredients_text = "、".join(ingredients)
    prompt = f"""以下の材料を使った美味しい料理を1つ提案してください：
材料: {ingredients_text}

以下のJSON形式で回答してください（他の文章は含めずにJSONのみで回答）：

{{
  "dish_name": "料理名",
  "additional_ingredients": "追加で必要な材料（なければ「なし」）",
  "description": "料理の簡単な説明（1-2行）"
}}

例：
{{
  "dish_name": "鶏肉と野菜の炒め物",
  "additional_ingredients": "醤油、ごま油、塩コショウ",
  "description": "鶏肉と野菜をごま油で炒めた栄養バランスの良い一品です。短時間で作れて、ご飯との相性も抜群です。"
}}"""

    # APIキーを設定
    genai.configure(api_key=api_key)
    # モデルを作成
    model = genai.GenerativeModel("gemini-2.5-flash")

    # リトライ機能付きでAPI呼び出し
    for attempt in range(max_retries):
        try:

            # コンテンツを生成
            response = model.generate_content(prompt)

            if response and response.text:
                # JSON応答を解析
                try:
                    # レスポンステキストからJSONを抽出（```jsonタグが含まれている場合もある）
                    clean_text = response.text.strip()
                    if clean_text.startswith("```json"):
                        clean_text = (
                            clean_text.replace("```json", "").replace("```", "").strip()
                        )
                    elif clean_text.startswith("```"):
                        clean_text = clean_text.replace("```", "").strip()

                    recipe_data = json.loads(clean_text)

                    return {
                        "error": False,
                        "dish_name": recipe_data.get("dish_name", "料理名不明"),
                        "additional_ingredients": recipe_data.get(
                            "additional_ingredients", "不明"
                        ),
                        "description": recipe_data.get("description", "説明なし"),
                        "ingredients_used": ingredients,
                        "raw_text": response.text,
                    }
                except json.JSONDecodeError:
                    # JSON解析に失敗した場合は元のテキストを返す
                    return {
                        "error": False,
                        "recipe_text": response.text,
                        "ingredients_used": ingredients,
                    }
            else:
                raise Exception("APIから有効な応答を受信できませんでした")
        except Exception as e:
            print(f"API呼び出しエラー: {str(e)}")
            if attempt < max_retries - 1:  # 最後の試行でない場合
                continue
            else:
                return {
                    "error": True,
                    "message": f"API呼び出しに失敗しました: {str(e)}",
                }

    return {"error": True, "message": "予期しないエラーが発生しました"}


@login_required
def index(request):
    form = IngredientForm()
    context = {"form": form}

    if request.method == "POST":
        form = IngredientForm(request.POST)
        context["form"] = form

        if form.is_valid():
            # フォームから材料を取得
            ingredients = form.get_ingredients_list()

            if not ingredients:
                messages.error(request, "最低1つの材料を入力してください。")
            else:
                # Gemini APIを呼び出し
                result = call_gemini_api(ingredients)

                if result["error"]:
                    messages.error(request, result["message"])
                else:
                    context["recipe_result"] = result
                    messages.success(request, "料理を提案しました！")
        else:
            messages.error(request, "入力内容に問題があります。")

    return render(request, "work11/index.html", context)
