"""
CSV file handling utilities for data persistence
Provides functions for reading, writing, and managing CSV data across the application
"""

import pandas as pd
import os
import datetime
import streamlit as st
from typing import Dict, List, Any, Optional

def save_to_csv(filename: str, data: Dict[str, Any], append: bool = True) -> bool:
    """
    Save data to CSV file
    
    Args:
        filename: Name of the CSV file
        data: Dictionary containing the data to save
        append: Whether to append to existing file or overwrite
        
    Returns:
        bool: Success status
    """
    try:
        # Convert single record to DataFrame
        new_df = pd.DataFrame([data])
        
        # Check if file exists and we want to append
        if append and os.path.exists(filename):
            # Append to existing file
            new_df.to_csv(filename, mode='a', header=False, index=False)
        else:
            # Create new file or overwrite
            new_df.to_csv(filename, index=False)
        
        return True
        
    except Exception as e:
        st.error(f"Failed to save data to {filename}: {str(e)}")
        return False

def load_from_csv(filename: str) -> pd.DataFrame:
    """
    Load data from CSV file
    
    Args:
        filename: Name of the CSV file
        
    Returns:
        pandas.DataFrame: Loaded data or empty DataFrame if file doesn't exist
    """
    try:
        if os.path.exists(filename):
            df = pd.read_csv(filename)
            return df
        else:
            # Return empty DataFrame with no columns
            return pd.DataFrame()
            
    except Exception as e:
        st.warning(f"Failed to load data from {filename}: {str(e)}")
        return pd.DataFrame()

def update_csv_record(filename: str, record_id: str, id_column: str, updates: Dict[str, Any]) -> bool:
    """
    Update a specific record in CSV file
    
    Args:
        filename: Name of the CSV file
        record_id: ID of the record to update
        id_column: Name of the ID column
        updates: Dictionary of field updates
        
    Returns:
        bool: Success status
    """
    try:
        df = load_from_csv(filename)
        
        if df.empty:
            st.warning(f"No data found in {filename}")
            return False
        
        # Find the record to update
        mask = df[id_column] == record_id
        
        if not mask.any():
            st.warning(f"Record with {id_column} = {record_id} not found")
            return False
        
        # Update the record
        for field, value in updates.items():
            df.loc[mask, field] = value
        
        # Add timestamp of update
        df.loc[mask, 'last_updated'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Save updated DataFrame
        df.to_csv(filename, index=False)
        
        return True
        
    except Exception as e:
        st.error(f"Failed to update record in {filename}: {str(e)}")
        return False

def delete_csv_record(filename: str, record_id: str, id_column: str) -> bool:
    """
    Delete a specific record from CSV file
    
    Args:
        filename: Name of the CSV file
        record_id: ID of the record to delete
        id_column: Name of the ID column
        
    Returns:
        bool: Success status
    """
    try:
        df = load_from_csv(filename)
        
        if df.empty:
            st.warning(f"No data found in {filename}")
            return False
        
        # Find and remove the record
        mask = df[id_column] == record_id
        
        if not mask.any():
            st.warning(f"Record with {id_column} = {record_id} not found")
            return False
        
        # Remove the record
        df = df[~mask]
        
        # Save updated DataFrame
        df.to_csv(filename, index=False)
        
        return True
        
    except Exception as e:
        st.error(f"Failed to delete record from {filename}: {str(e)}")
        return False

def search_csv_records(filename: str, search_criteria: Dict[str, Any]) -> pd.DataFrame:
    """
    Search for records in CSV file based on criteria
    
    Args:
        filename: Name of the CSV file
        search_criteria: Dictionary of search criteria
        
    Returns:
        pandas.DataFrame: Filtered results
    """
    try:
        df = load_from_csv(filename)
        
        if df.empty:
            return df
        
        # Apply search criteria
        for column, value in search_criteria.items():
            if column in df.columns:
                if isinstance(value, str):
                    # String search (case-insensitive, partial match)
                    df = df[df[column].astype(str).str.contains(value, case=False, na=False)]
                else:
                    # Exact match for non-string values
                    df = df[df[column] == value]
        
        return df
        
    except Exception as e:
        st.error(f"Failed to search records in {filename}: {str(e)}")
        return pd.DataFrame()

def get_csv_statistics(filename: str) -> Dict[str, Any]:
    """
    Get statistics about CSV file
    
    Args:
        filename: Name of the CSV file
        
    Returns:
        dict: Statistics about the file
    """
    try:
        if not os.path.exists(filename):
            return {'exists': False}
        
        df = load_from_csv(filename)
        
        stats = {
            'exists': True,
            'record_count': len(df),
            'column_count': len(df.columns),
            'columns': df.columns.tolist(),
            'file_size_bytes': os.path.getsize(filename),
            'file_size_kb': round(os.path.getsize(filename) / 1024, 2),
            'last_modified': datetime.datetime.fromtimestamp(
                os.path.getmtime(filename)
            ).strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # Add data type information
        if not df.empty:
            stats['data_types'] = df.dtypes.to_dict()
            stats['memory_usage_mb'] = round(df.memory_usage(deep=True).sum() / 1024 / 1024, 2)
        
        return stats
        
    except Exception as e:
        st.warning(f"Failed to get statistics for {filename}: {str(e)}")
        return {'exists': False, 'error': str(e)}

def backup_csv_file(filename: str, backup_suffix: Optional[str] = None) -> str:
    """
    Create backup of CSV file
    
    Args:
        filename: Name of the CSV file to backup
        backup_suffix: Optional suffix for backup filename
        
    Returns:
        str: Backup filename or empty string if failed
    """
    try:
        if not os.path.exists(filename):
            st.warning(f"File {filename} does not exist")
            return ""
        
        # Generate backup filename
        if backup_suffix:
            backup_filename = f"{filename}.{backup_suffix}.bak"
        else:
            timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_filename = f"{filename}.{timestamp}.bak"
        
        # Copy file content
        df = load_from_csv(filename)
        df.to_csv(backup_filename, index=False)
        
        return backup_filename
        
    except Exception as e:
        st.error(f"Failed to backup {filename}: {str(e)}")
        return ""

def merge_csv_files(filenames: List[str], output_filename: str, remove_duplicates: bool = True) -> bool:
    """
    Merge multiple CSV files into one
    
    Args:
        filenames: List of CSV filenames to merge
        output_filename: Output filename for merged data
        remove_duplicates: Whether to remove duplicate records
        
    Returns:
        bool: Success status
    """
    try:
        merged_df = pd.DataFrame()
        
        for filename in filenames:
            if os.path.exists(filename):
                df = load_from_csv(filename)
                if not df.empty:
                    merged_df = pd.concat([merged_df, df], ignore_index=True)
        
        if merged_df.empty:
            st.warning("No data to merge")
            return False
        
        # Remove duplicates if requested
        if remove_duplicates:
            merged_df = merged_df.drop_duplicates()
        
        # Save merged data
        merged_df.to_csv(output_filename, index=False)
        
        return True
        
    except Exception as e:
        st.error(f"Failed to merge CSV files: {str(e)}")
        return False

def export_filtered_data(filename: str, filters: Dict[str, Any], export_filename: str) -> bool:
    """
    Export filtered data to new CSV file
    
    Args:
        filename: Source CSV filename
        filters: Dictionary of filters to apply
        export_filename: Output filename for filtered data
        
    Returns:
        bool: Success status
    """
    try:
        filtered_df = search_csv_records(filename, filters)
        
        if filtered_df.empty:
            st.warning("No records match the filter criteria")
            return False
        
        filtered_df.to_csv(export_filename, index=False)
        
        return True
        
    except Exception as e:
        st.error(f"Failed to export filtered data: {str(e)}")
        return False

def validate_csv_structure(filename: str, required_columns: List[str]) -> Dict[str, Any]:
    """
    Validate CSV file structure against required columns
    
    Args:
        filename: Name of the CSV file
        required_columns: List of required column names
        
    Returns:
        dict: Validation results
    """
    try:
        df = load_from_csv(filename)
        
        if df.empty:
            return {
                'valid': False,
                'error': 'File is empty or does not exist',
                'missing_columns': required_columns,
                'extra_columns': []
            }
        
        existing_columns = set(df.columns)
        required_columns_set = set(required_columns)
        
        missing_columns = list(required_columns_set - existing_columns)
        extra_columns = list(existing_columns - required_columns_set)
        
        validation_result = {
            'valid': len(missing_columns) == 0,
            'missing_columns': missing_columns,
            'extra_columns': extra_columns,
            'record_count': len(df),
            'column_count': len(df.columns)
        }
        
        if not validation_result['valid']:
            validation_result['error'] = f"Missing required columns: {missing_columns}"
        
        return validation_result
        
    except Exception as e:
        return {
            'valid': False,
            'error': str(e),
            'missing_columns': required_columns,
            'extra_columns': []
        }

def clean_csv_data(filename: str, clean_operations: List[str] = None) -> bool:
    """
    Clean CSV data by applying various operations
    
    Args:
        filename: Name of the CSV file
        clean_operations: List of operations to perform
        
    Returns:
        bool: Success status
    """
    try:
        df = load_from_csv(filename)
        
        if df.empty:
            st.warning(f"No data found in {filename}")
            return False
        
        if clean_operations is None:
            clean_operations = ['remove_duplicates', 'strip_whitespace', 'remove_empty_rows']
        
        original_count = len(df)
        
        # Apply cleaning operations
        if 'remove_duplicates' in clean_operations:
            df = df.drop_duplicates()
        
        if 'strip_whitespace' in clean_operations:
            # Strip whitespace from string columns
            string_columns = df.select_dtypes(include=['object']).columns
            df[string_columns] = df[string_columns].apply(lambda x: x.str.strip() if x.dtype == 'object' else x)
        
        if 'remove_empty_rows' in clean_operations:
            df = df.dropna(how='all')
        
        if 'standardize_dates' in clean_operations:
            # Attempt to standardize date columns
            for column in df.columns:
                if 'date' in column.lower() or 'time' in column.lower():
                    try:
                        df[column] = pd.to_datetime(df[column])
                    except:
                        pass  # Skip if conversion fails
        
        # Save cleaned data
        df.to_csv(filename, index=False)
        
        cleaned_count = len(df)
        st.success(f"Cleaned {filename}: {original_count} → {cleaned_count} records")
        
        return True
        
    except Exception as e:
        st.error(f"Failed to clean {filename}: {str(e)}")
        return False

def generate_csv_report(filename: str) -> Dict[str, Any]:
    """
    Generate comprehensive report about CSV file
    
    Args:
        filename: Name of the CSV file
        
    Returns:
        dict: Comprehensive report
    """
    try:
        stats = get_csv_statistics(filename)
        
        if not stats['exists']:
            return stats
        
        df = load_from_csv(filename)
        
        report = stats.copy()
        
        if not df.empty:
            # Add data quality metrics
            report['data_quality'] = {
                'null_counts': df.isnull().sum().to_dict(),
                'null_percentages': (df.isnull().sum() / len(df) * 100).round(2).to_dict(),
                'duplicate_rows': df.duplicated().sum(),
                'unique_counts': df.nunique().to_dict()
            }
            
            # Add sample data
            report['sample_data'] = {
                'first_5_rows': df.head().to_dict('records'),
                'last_5_rows': df.tail().to_dict('records')
            }
            
            # Add numeric column statistics
            numeric_columns = df.select_dtypes(include=['number']).columns.tolist()
            if numeric_columns:
                report['numeric_stats'] = df[numeric_columns].describe().to_dict()
        
        return report
        
    except Exception as e:
        return {'exists': False, 'error': str(e)}

def schedule_csv_cleanup(filenames: List[str], max_age_days: int = 30) -> Dict[str, int]:
    """
    Clean up old CSV files based on age
    
    Args:
        filenames: List of CSV filenames to check
        max_age_days: Maximum age in days before cleanup
        
    Returns:
        dict: Cleanup results
    """
    results = {
        'checked': 0,
        'cleaned': 0,
        'errors': 0,
        'total_space_freed_mb': 0
    }
    
    try:
        cutoff_date = datetime.datetime.now() - datetime.timedelta(days=max_age_days)
        
        for filename in filenames:
            results['checked'] += 1
            
            try:
                if os.path.exists(filename):
                    file_modified = datetime.datetime.fromtimestamp(os.path.getmtime(filename))
                    
                    if file_modified < cutoff_date:
                        file_size = os.path.getsize(filename)
                        
                        # Create backup before deletion
                        backup_filename = backup_csv_file(filename, 'cleanup')
                        
                        if backup_filename:
                            os.remove(filename)
                            results['cleaned'] += 1
                            results['total_space_freed_mb'] += file_size / (1024 * 1024)
                            
                            st.info(f"Cleaned up {filename} (backed up as {backup_filename})")
                        
            except Exception as e:
                results['errors'] += 1
                st.warning(f"Error processing {filename}: {str(e)}")
        
        return results
        
    except Exception as e:
        st.error(f"Cleanup operation failed: {str(e)}")
        results['errors'] += 1
        return results
