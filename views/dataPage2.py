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

    # Group transactions by `Member_number` (unique shopper)
    st.write("Grouping transactions by `Member_number`...")
    transactions = data.groupby("Member_number")["itemDescription"].apply(list)
    st.write("Transactions have been grouped by `Member_number`, representing individual shoppers.")

    # Convert transactions into a one-hot encoded DataFrame
    item_set = set(data["itemDescription"].unique())  # All unique items
    one_hot_encoded = pd.DataFrame(
        [{item: (item in transaction) for item in item_set} for transaction in transactions]
    )
    # st.write("Data has been transformed into a one-hot encoded format, representing each item in the transactions.")

    # Apply Apriori algorithm
    st.subheader("Frequent Itemsets")
    frequent_itemsets = apriori(one_hot_encoded, min_support=min_support, use_colnames=True)
    if frequent_itemsets.empty:
        st.warning("No frequent itemsets found for the given support level. Try lowering the minimum support.")
    else:
        st.write("The table below lists the frequent itemsets discovered from the transactions. Each row shows an itemset, its support, and other relevant details.")
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
        st.write("This bar graph displays the top 20 most frequently purchased items in the dataset. The x-axis shows the item descriptions, while the y-axis represents their frequency.")

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
                st.write("The table below displays the association rules generated based on the given minimum confidence threshold. Each row includes the antecedent, consequent, support, confidence, lift, and other metrics.")
                st.write(rules)

                # Visualization of Association Rules (Confidence vs Lift)
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
                st.write("The scatter plot shows the relationship between confidence and lift for the association rules. Each point represents a rule, and its position reflects its confidence (x-axis) and lift (y-axis). Rules with higher lift are generally more meaningful.")

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
