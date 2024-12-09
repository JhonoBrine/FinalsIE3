# import streamlit as st
# import pandas as pd
# from mlxtend.frequent_patterns import apriori, association_rules

# # Streamlit app title
# st.title("Apriori Algorithm for Groceries Dataset")

# # Sidebar for parameters
# st.sidebar.header("Parameters")
# min_support = st.sidebar.slider("Minimum Support", 0.01, 1.0, 0.1)
# min_confidence = st.sidebar.slider("Minimum Confidence", 0.01, 1.0, 0.5)

# # Load the groceries dataset
# file_path = "assets/csv/Groceries_dataset.csv"  # Ensure this file is in the same directory
# try:
#     data = pd.read_csv(file_path)

#     # Display the raw dataset
#     st.subheader("Raw Dataset")
#     st.dataframe(data.head())

#     # Preprocess the dataset
#     st.subheader("Data Preprocessing")

#     # Convert 'Date' to datetime format
#     data['Date'] = pd.to_datetime(data['Date'])

#     # Combine Member_number and Date to create a unique transaction ID
#     data['transaction_id'] = data['Member_number'].astype(str) + "_" + data['Date'].dt.date.astype(str)

#     # Group by transaction_id and combine items into a list
#     transactions = data.groupby('transaction_id')['itemDescription'].apply(list).reset_index()

#     # Display the grouped transactions (preview)
#     st.write("Grouped transactions by transaction_id and Date:")
#     st.dataframe(transactions.head())

#     # One-hot encode the transactions
#     st.write("Transforming data into a one-hot encoded format...")
#     item_set = set(data['itemDescription'].unique())  # All unique items
#     one_hot_encoded = pd.DataFrame(
#         [{item: (item in transaction) for item in item_set} for transaction in transactions['itemDescription']]
#     )
#     one_hot_encoded['transaction_id'] = transactions['transaction_id']  # Keep transaction_id for reference

#     st.write("One-hot encoded data preview:")
#     st.dataframe(one_hot_encoded.head())

#     # Apply Apriori algorithm
#     st.subheader("Frequent Itemsets")
#     frequent_itemsets = apriori(one_hot_encoded.drop('transaction_id', axis=1), min_support=min_support, use_colnames=True)
#     if frequent_itemsets.empty:
#         st.warning("No frequent itemsets found for the given support level. Try lowering the minimum support.")
#     else:
#         st.write(frequent_itemsets)

#         # Generate association rules
#         st.subheader("Association Rules")
#         try:
#             # Check if 'num_itemsets' argument is needed
#             if "num_itemsets" in association_rules.__code__.co_varnames:
#                 rules = association_rules(
#                     frequent_itemsets, metric="confidence", min_threshold=min_confidence, num_itemsets=len(frequent_itemsets)
#                 )
#             else:
#                 rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=min_confidence)

#             if rules.empty:
#                 st.warning("No association rules found for the given confidence level. Try lowering the minimum confidence.")
#             else:
#                 st.write(rules)

#                 # Download link for results
#                 st.subheader("Download Results")
#                 csv = rules.to_csv(index=False).encode('utf-8')
#                 st.download_button(
#                     label="Download Rules as CSV",
#                     data=csv,
#                     file_name="association_rules.csv",
#                     mime="text/csv",
#                 )
#         except Exception as e:
#             st.error(f"An error occurred while generating association rules: {e}")

# except FileNotFoundError:
#     st.error(f"The file '{file_path}' was not found. Please ensure it is in the same folder as this script.")
# except Exception as e:
#     st.error(f"An error occurred: {e}")   

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from mlxtend.frequent_patterns import apriori, association_rules

# Streamlit app title
st.title("Apriori Algorithm for Groceries Dataset")

# Sidebar for parameters
st.sidebar.header("Parameters")
min_support = st.sidebar.slider("Minimum Support", 0.01, 1.0, 0.1)
min_confidence = st.sidebar.slider("Minimum Confidence", 0.01, 1.0, 0.5)

# Load the groceries dataset
file_path = "assets/csv/Groceries_dataset.csv"  # Ensure this file is in the same directory
try:
    data = pd.read_csv(file_path)

    # Display the raw dataset
    st.subheader("Raw Dataset")
    st.dataframe(data.head())

    # Preprocess the dataset
    st.subheader("Data Preprocessing")

    # Convert 'Date' to datetime format
    data['Date'] = pd.to_datetime(data['Date'])

    # Combine Member_number and Date to create a unique transaction ID
    data['transaction_id'] = data['Member_number'].astype(str) + "_" + data['Date'].dt.date.astype(str)

    # Group by transaction_id and combine items into a list
    transactions = data.groupby('transaction_id')['itemDescription'].apply(list).reset_index()

    # Display the grouped transactions (preview)
    st.write("Grouped transactions by transaction_id and Date:")
    st.dataframe(transactions.head())

    # One-hot encode the transactions
    st.write("Transforming data into a one-hot encoded format...")
    item_set = set(data['itemDescription'].unique())  # All unique items
    one_hot_encoded = pd.DataFrame(
        [{item: (item in transaction) for item in item_set} for transaction in transactions['itemDescription']]
    )
    one_hot_encoded['transaction_id'] = transactions['transaction_id']  # Keep transaction_id for reference

    st.write("One-hot encoded data preview:")
    st.dataframe(one_hot_encoded.head())

    # Apply Apriori algorithm
    st.subheader("Frequent Itemsets")
    frequent_itemsets = apriori(one_hot_encoded.drop('transaction_id', axis=1), min_support=min_support, use_colnames=True)
    if frequent_itemsets.empty:
        st.warning("No frequent itemsets found for the given support level. Try lowering the minimum support.")
    else:
        st.write(frequent_itemsets)

        # Visualization of Item Frequencies (Bar Graph for Item Frequencies)
        item_frequencies = data['itemDescription'].value_counts()
        st.subheader("Bar Graph of Item Frequencies")
        fig, ax = plt.subplots(figsize=(10, 6))
        item_frequencies.head(20).plot(kind='bar', ax=ax)  # Show top 20 items for clarity
        ax.set_title("Top 20 Most Frequent Items")
        ax.set_xlabel("Item Description")
        ax.set_ylabel("Frequency")
        ax.tick_params(axis='x', rotation=45)  # Rotate x-axis labels for better readability
        st.pyplot(fig)

        # Generate association rules
        st.subheader("Association Rules")
        try:
            # Check if 'num_itemsets' argument is needed
            if "num_itemsets" in association_rules.__code__.co_varnames:
                rules = association_rules(
                    frequent_itemsets, metric="confidence", min_threshold=min_confidence, num_itemsets=len(frequent_itemsets)
                )
            else:
                rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=min_confidence)

            if rules.empty:
                st.warning("No association rules found for the given confidence level. Try lowering the minimum confidence.")
            else:
                st.write(rules)

                # Visualization of Association Rules (Confidence and Lift)
                st.subheader("Metrics for Association Rules")

                # Plot Confidence vs Lift
                fig, ax = plt.subplots(figsize=(10, 6))
                sns.scatterplot(x='confidence', y='lift', data=rules, ax=ax)

                # Label each dot with its corresponding row number ("Row #")
                for i, row in rules.iterrows():
                    ax.text(
                        row['confidence'], row['lift'], 
                        f"Row {i+1}",  # Add row number (starting from 1)
                        horizontalalignment='left', 
                        size='small', 
                        color='black'
                    )

                ax.set_title("Confidence vs Lift for Association Rules")
                ax.set_xlabel("Confidence")
                ax.set_ylabel("Lift")
                st.pyplot(fig)

                # Download link for results
                st.subheader("Download Results")
                csv = rules.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="Download Rules as CSV",
                    data=csv,
                    file_name="association_rules.csv",
                    mime="text/csv",
                )
        except Exception as e:
            st.error(f"An error occurred while generating association rules: {e}")

except FileNotFoundError:
    st.error(f"The file '{file_path}' was not found. Please ensure it is in the same folder as this script.")
except Exception as e:
    st.error(f"An error occurred: {e}")