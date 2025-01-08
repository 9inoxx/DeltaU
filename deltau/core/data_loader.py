import pandas as pd

def load_data(file_path, delimiter=None, parse_dates=True, date_column=None):
    """
    Loads data from a .csv or .txt file into a Pandas DataFrame.
    
    Parameters:
        file_path (str): Path to the .csv or .txt file.
        delimiter (str, optional): Delimiter used in the file (e.g., ',' for CSV or '\t' for tab-separated files).
        If None, pandas will try to infer the delimiter.
        parse_dates (bool): Whether to parse dates. Defaults to True.
        date_column (str or list, optional): Column(s) to parse as dates. If None, auto-detects based on format.
    
    Returns:
        pd.DataFrame: A DataFrame containing the loaded data.
    
    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file extension is unsupported.
    """
    try:
        # Determine delimiter if not provided
        if delimiter is None:
            delimiter = ',' if file_path.endswith('.csv') else '\t'
        
        # Load the file into a DataFrame
        df = pd.read_csv(file_path, delimiter=delimiter, parse_dates=parse_dates, infer_datetime_format=True)

        # Parse specific date columns if provided
        if parse_dates and date_column is not None:
            df[date_column] = pd.to_datetime(df[date_column])

        print(f"Data loaded successfully from {file_path}. Shape: {df.shape}")
        return df

    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    
    except pd.errors.ParserError as e:
        raise ValueError(f"Parsing error: {e}")
    
    except Exception as e:
        raise ValueError(f"An error occurred while loading the file: {e}")
