import pandas as pd
import os
from dotenv import load_dotenv
from hindsight_client import Hindsight

# Load .env
load_dotenv()

# Keys
HINDSIGHT_API_KEY = os.getenv("HINDSIGHT_API_KEY")
BANK_NAME = "hacathon"

def main():
    try:
        # CSV read karte waqt extra commas ko handle karne ke liye
        df = pd.read_csv("faq_data.csv", on_bad_lines='skip')
        
        # 2. Yahan base_url add kiya hai taaki error na aaye
        client = Hindsight(
            api_key=HINDSIGHT_API_KEY, 
            base_url="https://api.hindsight.vectorize.io"
        )
        
        uploaded_count = 0
        for _, row in df.iterrows():
            question = str(row.get("Question", ""))
            answer = str(row.get("Answer", ""))
            
            if question and answer:
                content = f"Q: {question}\nA: {answer}"
                # 3. 'bank_id' use karein
                client.retain(content=content, bank_id=BANK_NAME)
                print(f"Uploaded: {question[:50]}...")
                uploaded_count += 1
        
        print(f"\nSuccessfully uploaded {uploaded_count} items to Hindsight!")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()