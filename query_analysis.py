import pandas as pd
import re
from collections import Counter
from itertools import combinations

def extract_keywords(queries):
    # Updated pattern to include dots in keywords
    
    pattern = r'\b[@\w.]+\b(?=:)'
    keyword_list=[]
    for query in queries:
        cleaned = re.sub(r'"[^"]*"', '', query)

        # Extract all keywords using regex
        keywords = re.findall(pattern, cleaned)

        keywords = [s for s in keywords if len(s) <= 25] # Filter out long keywords

        # Use a set to avoid duplicates and convert back to list if needed
        keyword_list.append(set(keywords))
    return keyword_list

def analyze_query_filters(csv_file):
    # Load CSV file
    df = pd.read_csv(csv_file)

    if 'query_Query' not in df.columns:
        df.rename(columns={'query': 'query_Query'}, inplace=True)

    # Extract the queries column
    queries = df['query_Query'].dropna()  # Drop NaN values to avoid errors
    
    stars=1
    
    for q in queries:
        if "*"  in q:
            stars+=1
    
    print('Star count:',stars)
    print('Star percentage:',stars/len(queries)*100)


    query_filters = extract_keywords(queries)

    all_filters = [token for query in query_filters for token in query]

    # Count occurrences of each filter
    filter_counts = Counter(all_filters)
    
    # Calculate percentage of queries containing each filter
    total_queries = len(queries)
    filter_percentages = {key: (value / total_queries) * 100 for key, value in filter_counts.items()}
    
    # Convert results to DataFrame for better visualization
    filter_results_df = pd.DataFrame({
        'Token': filter_counts.keys(),
        'Count': filter_counts.values(),
        'Percentage': filter_percentages.values()
    }).sort_values(by='Count', ascending=False)

    #remove empty sets
    query_filters=[x for x in query_filters if len(x)>0]

    # Convert sets to frozensets for counting
    frozenset_list = [frozenset(x) for x in query_filters]
    query_filter_dict={}

  
    

    for f in frozenset_list:
        if f in query_filter_dict:
            query_filter_dict[f]+=1
        else:
            query_filter_dict[f]=1



    token_tuples = [f"{{{', '.join(key)}}}" for key in query_filter_dict.keys()]

    # Convert tuple counts to DataFrame
    tuple_results_df = pd.DataFrame({
        'Token Tuple': token_tuples,
        'Count': query_filter_dict.values(),
        'Percentage': [value / total_queries * 100 for value in query_filter_dict.values()]
    }).sort_values(by='Count', ascending=False)
    
    return filter_results_df, tuple_results_df

if __name__ == "__main__":
    csv_file_all = "Casem queries - All queries.csv"  
    # csv_file_all = "a.csv"  

    result_all,tuple_results_all = analyze_query_filters(csv_file_all)
    result_all.to_csv("filter_analysis - All Queries.csv", index=False)
    tuple_results_all.to_csv("tuple_analysis - All Queries.csv", index=False)

    csv_file_cm = "Casem queries - Case Management Queries.csv"  
    result_cm,tuple_results_cm = analyze_query_filters(csv_file_cm)
    result_cm.to_csv("filter_analysis - Case Management Queries.csv", index=False)
    tuple_results_cm.to_csv("tuple_analysis - Case Management Queries.csv", index=False)

