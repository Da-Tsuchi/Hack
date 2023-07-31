from django import forms

# 年月を選択するフォーム
class MonthYearForm(forms.Form):
    YEARS = [(year, year) for year in range(2023, 2100)]
    MONTHS = [(month, month) for month in range(1, 13)]
    year = forms.ChoiceField(choices=YEARS)
    month = forms.ChoiceField(choices=MONTHS)
    