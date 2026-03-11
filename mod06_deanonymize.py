import pandas as pd

def load_data(anonymized_path, auxiliary_path):
    """
    Load anonymized and auxiliary datasets.
    """
    anon = pd.read_csv(anonymized_path)
    aux = pd.read_csv(auxiliary_path)
    return anon, aux


def link_records(anon_df, aux_df):
    """
    Attempt to link anonymized records to auxiliary records
    using exact matching on quasi-identifiers.

    Returns a DataFrame with columns:
      anon_id, matched_name
    containing ONLY uniquely matched records.
    """
    # common columns
    common_cols = list(set(anon_df.columns) & set(aux_df.columns))
    common_cols = [c for c in common_cols if c not in ['anon_id', 'name']]

    # merge
    merged = pd.merge(anon_df, aux_df, on=common_cols)

    # filter
    unique_matches = merged.groupby('anon_id').filter(lambda x: len(x) == 1)
    result = unique_matches[['anon_id', 'name']].rename(columns={'name': 'matched_name'})
    
    return result
def deanonymization_rate(matches_df, anon_df):
    """
    Compute the fraction of anonymized records
    that were uniquely re-identified.
    """
    if anon_df.empty:
        return 0.0
    
    rate = len(matches_df) / len(anon_df)
    return rate