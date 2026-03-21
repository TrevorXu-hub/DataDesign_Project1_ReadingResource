from pathlib import Path
import zipfile
import pandas as pd


RAW_DIR = Path("data/raw")
ZIP_PATH = RAW_DIR / "default+of+credit+card+clients.zip"
EXTRACTED_XLS = RAW_DIR / "default of credit card clients.xls"


def extract_zip(zip_path: Path, output_dir: Path) -> None:
    if not zip_path.exists():
        raise FileNotFoundError(f"Could not find zip file: {zip_path}")
    with zipfile.ZipFile(zip_path, "r") as z:
        z.extractall(output_dir)


def load_raw_data(xls_path: Path) -> pd.DataFrame:
    if not xls_path.exists():
        raise FileNotFoundError(f"Could not find Excel file: {xls_path}")
    # header=1 because the real column names start on the second row
    df = pd.read_excel(xls_path, header=1)
    return df


def main() -> None:
    print("Extracting raw zip file...")
    extract_zip(ZIP_PATH, RAW_DIR)

    print("Loading Excel file...")
    df = load_raw_data(EXTRACTED_XLS)

    print("\n===== BASIC INFO =====")
    print("Shape:", df.shape)

    print("\n===== COLUMN NAMES =====")
    print(df.columns.tolist())

    print("\n===== FIRST 5 ROWS =====")
    print(df.head())

    print("\n===== DATA TYPES =====")
    print(df.dtypes)

    print("\n===== MISSING VALUES =====")
    print(df.isna().sum())

    if "ID" in df.columns:
        print("\nDuplicate IDs:", df["ID"].duplicated().sum())

    print("\n===== TARGET DISTRIBUTION =====")
    target_col = "default payment next month"
    if target_col in df.columns:
        print(df[target_col].value_counts(dropna=False))
        print(df[target_col].value_counts(normalize=True, dropna=False))


if __name__ == "__main__":
    main()
