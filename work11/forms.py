from django import forms


class IngredientForm(forms.Form):
    ingredient1 = forms.CharField(
        max_length=50,
        required=True,
        label="材料 1 (必須)",
        widget=forms.TextInput(
            attrs={"placeholder": "例: 鶏肉", "class": "form-control"}
        ),
    )

    ingredient2 = forms.CharField(
        max_length=50,
        required=False,
        label="材料 2",
        widget=forms.TextInput(
            attrs={"placeholder": "例: 玉ねぎ", "class": "form-control"}
        ),
    )

    ingredient3 = forms.CharField(
        max_length=50,
        required=False,
        label="材料 3",
        widget=forms.TextInput(
            attrs={"placeholder": "例: じゃがいも", "class": "form-control"}
        ),
    )

    ingredient4 = forms.CharField(
        max_length=50,
        required=False,
        label="材料 4",
        widget=forms.TextInput(
            attrs={"placeholder": "例: 人参", "class": "form-control"}
        ),
    )

    ingredient5 = forms.CharField(
        max_length=50,
        required=False,
        label="材料 5",
        widget=forms.TextInput(
            attrs={"placeholder": "例: しめじ", "class": "form-control"}
        ),
    )

    def get_ingredients_list(self):
        """入力された材料のリストを取得"""
        ingredients = []
        for i in range(1, 6):
            ingredient = self.cleaned_data.get(f"ingredient{i}")
            if ingredient and ingredient.strip():
                ingredients.append(ingredient.strip())
        return ingredients
