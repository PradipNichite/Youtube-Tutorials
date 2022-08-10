from fastapi import FastAPI,Request
# from pydantic import BaseModel
import uvicorn
import numpy as np
from transformers import BertTokenizer, BertForSequenceClassification
import torch

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/hello")
def read_root():
    return {"Hello": "Hello"}

def get_model():
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    model = BertForSequenceClassification.from_pretrained("pnichite/YTFineTuneBert")
    return tokenizer,model

d = {
    
  1:'Toxic',
  0:'Non Toxic'
}

tokenizer,model = get_model()

@app.post("/predict")
async def read_root(request: Request):
    data = await request.json()
    print(data)
    if 'text' in data:
        user_input = data['text']
        test_sample = tokenizer([user_input], padding=True, truncation=True, max_length=512,return_tensors='pt')
        output = model(**test_sample)
        y_pred = np.argmax(output.logits.detach().numpy(),axis=1)  
        response = {"Recieved Text": user_input,"Prediction": d[y_pred[0]]}
    else:
        response = {"Recieved Text": "No Text Found"}
    return response

if __name__ == "__main__":
    uvicorn.run("main:app",host='0.0.0.0', port=8080, reload=True, debug=True)


