from pathlib import Path
import zipfile
import pandas as pd


RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")

ZIP_PATH = RAW_DIR / "default+of+credit+card+clients.zip"
EXTRACTED_XLS = RAW_DIR / "default of credit card clients.xls"
OUTPUT_CSV = PROCESSED_DIR / "credit_default_cleaned.csv"


def extract_zip(zip_path: Path, output_dir: Path) -> None:
    if not zip_path.exists():
        raise FileNotFoundError(f"Could not find zip file: {zip_path}")
    with zipfile.ZipFile(zip_path, "r") as z:
        z.extractall(output_dir)


def load_raw_data(xls_path: Path) -> pd.DataFrame:
    if not xls_path.exists():
        raise FileNotFoundError(f"Could not find Excel file: {xls_path}")
    df = pd.read_excel(xls_path, header=1)
    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    # Rename target column to something easier to use
    df = df.rename(columns={"default payment next month": "default_next_month"})

    # Optional: make column names lowercase
    df.columns = [col.lower() for col in df.columns]

    # Treat coded variables as categories
    cat_cols = ["sex", "education", "marriage"]
    for col in cat_cols:
        df[col] = df[col].astype("category")

    # Optional small cleaning for unusual education / marriage codes
    # education: 0, 5, 6 can be grouped into 4 = "other"
    df["education"] = df["education"].replace({0: 4, 5: 4, 6: 4})

    # marriage: 0 can be grouped into 3 = "other"
    df["marriage"] = df["marriage"].replace({0: 3})

    # Convert back to category after replacement
    df["education"] = df["education"].astype("category")
    df["marriage"] = df["marriage"].astype("category")

    # Remove ID from modeling later if needed, but keep it in cleaned file
    # because it is still useful as a record identifier
    return df


def main() -> None:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    print("Extracting raw zip file...")
    extract_zip(ZIP_PATH, RAW_DIR)

    print("Loading Excel file...")
    df = load_raw_data(EXTRACTED_XLS)

    print("Cleaning dataset...")
    cleaned_df = clean_data(df)

    print("\n===== CLEANED INFO =====")
    print("Shape:", cleaned_df.shape)
    print(cleaned_df.dtypes)

    print("\n===== MISSING VALUES =====")
    print(cleaned_df.isna().sum())

    print("\nSaving cleaned dataset to:", OUTPUT_CSV)
    cleaned_df.to_csv(OUTPUT_CSV, index=False)

    print("\nDone.")
    print(cleaned_df.head())


if __name__ == "__main__":
    main()
