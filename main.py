import requests
import pandas as pd
from sqlalchemy import create_engine
import sys # We'll use this to exit if the database fails

# --- DATABASE CONNECTION DETAILS ---
# !! IMPORTANT: Change this to the password you created on Day 1 !!
DB_PASSWORD = "1402" 
# -----------------------------------

DB_USER = "postgres"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "article_db"
API_URL = "https://saurav.tech/NewsAPI/top-headlines/category/technology/in.json"

def fetch_data(url):
    """Fetches data from the API."""
    print("Fetching data from API...")
    try:
        response = requests.get(url)
        response.raise_for_status() 
        print("Data fetched successfully!")
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def transform_data(data):
    """Transforms the raw data into a clean DataFrame."""
    if data is None or data.get('status') != 'ok':
        print("No valid data to transform.")
        return None
        
    articles = data.get('articles', [])
    
    if not isinstance(articles, list):
        print("Data format error: 'articles' is not a list.")
        return None

    print(f"Received {len(articles)} articles. Transforming...")
    
    df = pd.DataFrame(articles)
    
    columns_to_keep = ['title', 'description', 'url']
    
    # Check for columns and filter
    existing_cols = [col for col in columns_to_keep if col in df.columns]
    if 'description' not in existing_cols:
        print("Error: 'description' column (for text_content) is missing. Cannot proceed.")
        return None
        
    df = df[existing_cols]
    
    # Rename 'description' to 'text_content' to match our database
    df = df.rename(columns={'description': 'text_content'})
    
    # Clean up "damaged packages"
    df = df.dropna(subset=['title', 'text_content'])
    
    # Remove articles with placeholder content
    df = df[df['text_content'] != '[Removed]']
    
    print(f"Transformation complete. {len(df)} clean articles ready.")
    return df

# --- NEW FUNCTION ---
def load_data(df):
    """Loads the clean DataFrame into the PostgreSQL database."""
    print("Connecting to database...")
    try:
        # Create the "connection string"
        # This is like the database's full, private address
        # format: "postgresql://user:password@host:port/database_name"
        db_url = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        
        # Create the "engine" (the connection manager)
        engine = create_engine(db_url)
        
        print("Loading data into 'articles' table...")
        
        # This is the magic pandas command!
        df.to_sql(
            name='articles',    # The name of our table in pgAdmin
            con=engine,         # The connection engine we just made
            if_exists='append', # 'append' means add new data. 'replace' would wipe it out.
            index=False         # Don't save the pandas index (0, 1, 2...) as a column
        )
        
        print("Data loaded successfully!")
    
    except Exception as e:
        print(f"Error connecting or loading data: {e}")
        print("Please check your DB_PASSWORD in the script and that PostgreSQL is running.")
        sys.exit(1) # Exit the script if the database part fails

# --- UPDATED MAIN SCRIPT ---
if __name__ == "__main__":
    raw_data = fetch_data(API_URL)
    clean_articles_df = transform_data(raw_data)
    
    if clean_articles_df is not None:
        print("\n--- Clean Articles Ready for Database ---")
        print(clean_articles_df.head()) # .head() prints just the first 5
        print("-----------------------------------------")
        
        # This is our new "L" step
        load_data(clean_articles_df)
        
    else:
        print("No data to load.")