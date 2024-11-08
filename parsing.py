import os
import requests
import pandas as pd
from io import BytesIO
import matplotlib.pyplot as plt
from datetime import datetime

group_name = "ИСиП-21"

def download_and_generate_schedule():
    today = datetime.now()
    day_month = int(today.strftime("%d%m"))

    url = f"https://altask.ru/images/raspisanie/DO/{day_month}.xls"
    response = requests.get(url)
    file_content = response.content
    file = BytesIO(file_content)

    if url.endswith('.xls'):
        xlsx = pd.ExcelFile(file, engine="xlrd")
    elif url.endswith('.xlsx'):
        xlsx = pd.ExcelFile(file, engine="openpyxl")
    else:
        raise ValueError("Формат файла не поддерживается")

    found = False
    values = []

    for sheet_name in xlsx.sheet_names:
        df = xlsx.parse(sheet_name)
        for row_idx, row in df.iterrows():
            for col_idx, cell in enumerate(row):
                if str(cell).strip() == group_name:
                    found = True
                    start_row = row_idx
                    column = df.columns[col_idx]
                    values = df[column].iloc[start_row:start_row + 13].tolist()
                    break
            if found:
                break
        if found:
            break

    schedule = [val if pd.notna(val) else "" for val in values]
    merged_schedule = [schedule[0]]

    for i in range(1, len(schedule) - 1, 2):
        merged_schedule.append(f"{schedule[i]}\n{schedule[i + 1]}" if schedule[i] and schedule[i + 1] else schedule[i])

    df_schedule = pd.DataFrame(merged_schedule, columns=["Smerged_schedule"])

    fig, ax = plt.subplots(figsize=(6, len(merged_schedule) * 0.3))
    ax.axis('tight')
    ax.axis('off')
    table = ax.table(cellText=df_schedule.values, colLabels=df_schedule.columns, cellLoc='center', loc='center')

    table.auto_set_font_size(False)
    table.set_fontsize(10)
    for key, cell in table.get_celld().items():
        cell.set_height(0.3)
        cell.set_width(0.6)

    # Определяем путь к файлу
    output_path = os.path.abspath("schedule.png")
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close(fig)  # Закрываем фигуру, чтобы освободить память

    return output_path
