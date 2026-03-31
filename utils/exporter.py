import pandas as pd
import os

def export_to_csv(data, filename):
    os.makedirs("outputs", exist_ok=True)
    path = os.path.join("outputs", filename)
    df = pd.DataFrame(data)
    df.to_csv(path, index=False)
    return path