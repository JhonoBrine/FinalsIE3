import streamlit as st
import pandas as pd

# Streamlit app title
st.title("🛒 Groceries Dataset Analysis")

# Section 1: About the Dataset
st.header("📋 About the Groceries Dataset")
st.write("""
The Groceries Dataset consists of transaction data collected from a supermarket. 
Each transaction represents the items purchased by a customer during a shopping trip.

### Key Fields:
- **Member_number**: A unique identifier for a customer.
- **itemDescription**: The name of the purchased item.
- **Date**: The date of purchase.

Below is a sample of the dataset:
""")

# Load and display dataset
file_path = "assets/csv/Groceries_dataset.csv"  # Ensure this file is in the correct location
try:
    data = pd.read_csv(file_path)
    data_sample = data.head(10)  # Display the first 10 rows of the dataset
    st.dataframe(data_sample)

    st.write("""
    This dataset allows us to analyze relationships between purchased items, 
    enabling insights like frequently bought item combinations to guide marketing and inventory strategies.
    """)

except FileNotFoundError:
    st.error(f"❌ The file '{file_path}' was not found. Please ensure it is in the correct location.")
except Exception as e:
    st.error(f"❌ An error occurred while loading the dataset: {e}")

# Section 2: What is the Apriori Algorithm?
st.header("🔍 What is the Apriori Algorithm?")
st.write("""
The **Apriori Algorithm** is a popular data mining technique for identifying frequent itemsets in transactional datasets. 
It is widely applied in market basket analysis to uncover item combinations that frequently occur together.

### How it Works:
1. **Frequent Itemsets**: Identifies itemsets meeting a minimum support threshold.
2. **Association Rules**: Derives rules that indicate relationships between items.

### Key Metrics:
- **Support**: Proportion of transactions containing a specific item or itemset.
- **Confidence**: Likelihood of an item being purchased when another is purchased.
- **Lift**: Strength of an association rule compared to random chance.

For example:
If "bread" and "butter" appear together in 30% of transactions, and "bread" appears in 40%, 
then the confidence of the rule "bread → butter" is 75%.

Below is a simplified example of frequent itemsets:
""")

# Example of frequent itemsets table
example_data = {
    "Itemset": ["Bread, Butter", "Milk, Cookies", "Tea, Sugar"],
    "Support": [0.3, 0.25, 0.4],
}
example_df = pd.DataFrame(example_data)
st.table(example_df)

st.write("""
The Apriori Algorithm helps businesses uncover valuable insights into customer behavior, 
enabling strategies like product bundling, cross-selling, and personalized recommendations.
""")

# Footer: Invite users to explore the dataset further
st.info("📊 Use the sidebar to explore more about the dataset and its analysis.")
