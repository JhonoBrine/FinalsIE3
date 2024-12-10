# import streamlit as st
# import pandas as pd
# import seaborn as sns
# import matplotlib.pyplot as plt
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
#     # Data cleaning
#     data = data.dropna(subset=["Member_number", "itemDescription"])
#     data["itemDescription"] = data["itemDescription"].str.lower().str.strip()
#     data = data.drop_duplicates()

#     # Convert 'Date' to datetime format
#     data['Date'] = pd.to_datetime(data['Date'])

#     # Combine Member_number and Date to create a unique transaction ID
#     data['transaction_id'] = data['Member_number'].astype(str) + "_" + data['Date'].dt.date.astype(str)

#     # Group by transaction_id and combine items into a list
#     transactions = data.groupby('transaction_id')['itemDescription'].apply(list).reset_index()

#     # Display the grouped transactions (preview)
#     st.write("### Grouped Transactions by `transaction_id` and `Date`")
#     st.write("This table groups the data by transaction ID and date, showing the items bought in each transaction.")
#     st.write(transactions.head())

#     # One-hot encode the transactions
#     item_set = set(data['itemDescription'].unique())  # All unique items
#     one_hot_encoded = pd.DataFrame(
#         [{item: (item in transaction) for item in item_set} for transaction in transactions['itemDescription']]
#     )
#     one_hot_encoded['transaction_id'] = transactions['transaction_id']  # Keep transaction_id for reference
    
#     st.write("One-hot encoded data preview:")
#     st.dataframe(one_hot_encoded.head())

#     # Apply Apriori algorithm
#     st.subheader("Frequent Itemsets")
#     st.write("This section shows item combinations that are frequently purchased together based on the minimum support level. These itemsets help identify patterns in customer behavior.")
#     frequent_itemsets = apriori(one_hot_encoded.drop('transaction_id', axis=1), min_support=min_support, use_colnames=True)
#     if frequent_itemsets.empty:
#         st.warning("No frequent itemsets found for the given support level. Try lowering the minimum support.")
#     else:
#         st.write(frequent_itemsets)  # Display the frequent itemsets

#     # Bar Graph of Item Frequencies
#     item_frequencies = data['itemDescription'].value_counts()
#     st.subheader("Bar Graph of Item Frequencies")
#     st.write("This bar graph shows the top 20 most frequent items bought in the dataset. The x-axis shows the item names, and the y-axis shows how many times each item was bought.")
#     fig, ax = plt.subplots(figsize=(10, 6))
#     item_frequencies.head(20).plot(kind='bar', ax=ax)  # Show top 20 items for clarity
#     ax.set_title("Top 20 Most Frequent Items")
#     ax.set_xlabel("Item Description")
#     ax.set_ylabel("Frequency")
#     ax.tick_params(axis='x', rotation=45)  # Rotate x-axis labels for better readability
#     st.pyplot(fig)

#     # Generate association rules
#     st.subheader("Association Rules")
#     st.write("Association rules show relationships between items, such as 'if item A is bought, then item B is likely to be bought.' This section displays the rules generated based on the specified confidence level.")
#     try:
#         # Check if 'num_itemsets' argument is needed
#         if "num_itemsets" in association_rules.__code__.co_varnames:
#             rules = association_rules(
#                 frequent_itemsets, metric="confidence", min_threshold=min_confidence, num_itemsets=len(frequent_itemsets)
#             )
#         else:
#             rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=min_confidence)

#         if rules.empty:
#             st.warning("No association rules found for the given confidence level. Try lowering the minimum confidence.")
#         else:
#             st.write(rules)  # Display the association rules

#             # Metrics for Association Rules (Confidence vs Lift)
#             st.subheader("Metrics for Association Rules")
#             st.write("This scatter plot shows the relationship between the confidence and lift of the association rules. Confidence measures how often the consequent item is bought when the antecedent item is bought, while lift shows how much more likely the consequent item is purchased compared to random chance.")

#             # Plot Confidence vs Lift
#             fig, ax = plt.subplots(figsize=(10, 6))
#             sns.scatterplot(x='confidence', y='lift', data=rules, ax=ax)

#             # Label each dot with its corresponding row number ("Row #")
#             for i, row in rules.iterrows():
#                 ax.text(
#                     row['confidence'], row['lift'], 
#                     f"Row {i}",  # Add row number (starting from 1)
#                     horizontalalignment='left', 
#                     size='small', 
#                     color='black'
#                 )

#             ax.set_title("Confidence vs Lift for Association Rules")
#             ax.set_xlabel("Confidence")
#             ax.set_ylabel("Lift")
#             st.pyplot(fig)

#             # Download link for results
#             st.subheader("Download Results")
#             st.write("You can download the generated association rules as a CSV file.")
#             csv = rules.to_csv(index=False).encode('utf-8')
#             st.download_button(
#                 label="Download Rules as CSV",
#                 data=csv,
#                 file_name="association_rules.csv",
#                 mime="text/csv",
#             )
#     except Exception as e:
#         st.error(f"An error occurred while generating association rules: {e}")

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
    # Data cleaning
    data = data.dropna(subset=["Member_number", "itemDescription"])
    data["itemDescription"] = data["itemDescription"].str.lower().str.strip()
    data = data.drop_duplicates()

    # Convert 'Date' to datetime format
    data['Date'] = pd.to_datetime(data['Date'])

    # Combine Member_number and Date to create a unique transaction ID
    data['transaction_id'] = data['Member_number'].astype(str) + "_" + data['Date'].dt.date.astype(str)

    # Group by transaction_id and combine items into a list
    transactions = data.groupby('transaction_id')['itemDescription'].apply(list).reset_index()

    # Display the grouped transactions (preview)
    st.write("### Grouped Transactions by `transaction_id` and `Date`")
    st.write("This table groups the data by transaction ID and date, showing the items bought in each transaction.")
    st.write(transactions.head())

    # One-hot encode the transactions
    item_set = set(data['itemDescription'].unique())  # All unique items
    one_hot_encoded = pd.DataFrame(
        [{item: (item in transaction) for item in item_set} for transaction in transactions['itemDescription']]
    )
    one_hot_encoded['transaction_id'] = transactions['transaction_id']  # Keep transaction_id for reference
    
    st.write("One-hot encoded data preview:")
    st.dataframe(one_hot_encoded.head())

    # Apply Apriori algorithm
    st.subheader("Frequent Itemsets")
    st.write("This section shows item combinations that are frequently purchased together based on the minimum support level. These itemsets help identify patterns in customer behavior.")
    frequent_itemsets = apriori(one_hot_encoded.drop('transaction_id', axis=1), min_support=min_support, use_colnames=True)
    if frequent_itemsets.empty:
        st.warning("No frequent itemsets found for the given support level. Try lowering the minimum support.")
    else:
        st.write(frequent_itemsets)  # Display the frequent itemsets

        # Generate item frequency based on frequent itemsets
        st.subheader("Item Frequency from Frequent Itemsets")
        item_frequencies = (frequent_itemsets.explode('itemsets')
                            .groupby('itemsets')
                            .agg({'support': 'sum'})
                            .sort_values('support', ascending=False))

        # Reset index to make itemsets a column
        item_frequencies = item_frequencies.reset_index()
        item_frequencies.columns = ['Item', 'Support']

        st.write("This table shows the frequency of individual items based on the frequent itemsets identified.")
        st.dataframe(item_frequencies)

        # Bar Graph of Item Frequencies from Frequent Itemsets
        st.subheader("Bar Graph of Item Frequencies")
        st.write("This bar graph shows the top 20 most frequent items identified from the frequent itemsets. The x-axis shows the item names, and the y-axis shows their support values.")
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(data=item_frequencies.head(20), x='Support', y='Item', ax=ax)
        ax.set_title("Top 20 Most Frequent Items Based on Frequent Itemsets")
        ax.set_xlabel("Support")
        ax.set_ylabel("Item")
        st.pyplot(fig)

    # Generate association rules
    st.subheader("Association Rules")
    st.write("Association rules show relationships between items, such as 'if item A is bought, then item B is likely to be bought.' This section displays the rules generated based on the specified confidence level.")
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
            st.write(rules)  # Display the association rules

            # Metrics for Association Rules (Confidence vs Lift)
            st.subheader("Metrics for Association Rules")
            st.write("This scatter plot shows the relationship between the confidence and lift of the association rules. Confidence measures how often the consequent item is bought when the antecedent item is bought, while lift shows how much more likely the consequent item is purchased compared to random chance.")

            # Plot Confidence vs Lift
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.scatterplot(x='confidence', y='lift', data=rules, ax=ax)

            # Label each dot with its corresponding row number ("Row #")
            for i, row in rules.iterrows():
                ax.text(
                    row['confidence'], row['lift'], 
                    f"Row {i}",  # Add row number (starting from 1)
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
            st.write("You can download the generated association rules as a CSV file.")
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
