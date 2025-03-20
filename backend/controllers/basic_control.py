import pandas as pd

class BasicControl:
    @classmethod
    def select(cls)->str:
        df = pd.DataFrame({"col1":[1,2,3,4,5], "col2":[5,4,3,2,1]})
        json_response = df.to_json(orient="records")
        return json_response