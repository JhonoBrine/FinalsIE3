import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from mlxtend.frequent_patterns import apriori, association_rules

# Streamlit app title
st.title("Groceries Dataset Analysis with Recommendations and Conclusions")

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

    # Group transactions by `Member_number`
    transactions = data.groupby("Member_number")["itemDescription"].apply(list)

    # Convert transactions into a one-hot encoded DataFrame
    item_set = set(data["itemDescription"].unique())
    one_hot_encoded = pd.DataFrame(
        [{item: (item in transaction) for item in item_set} for transaction in transactions]
    )

    # Apply Apriori algorithm
    frequent_itemsets = apriori(one_hot_encoded, min_support=min_support, use_colnames=True)

    if frequent_itemsets.empty:
        st.warning("No frequent itemsets found for the given support level. Try lowering the minimum support.")
    else:
        st.subheader("Frequent Itemsets")
        st.write("Frequent itemsets represent combinations of items often purchased together.")
        st.write(frequent_itemsets)

        num_itemsets = len(transactions)

        # Generate association rules
        rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=min_confidence, num_itemsets=num_itemsets)

        if rules.empty:
            st.warning("No association rules found for the given confidence level. Try lowering the minimum confidence.")
        else:
            st.subheader("Association Rules")
            st.write("Association rules help identify relationships between items in transactions.")
            st.write(rules)

            # Visualization of Item Frequencies
            item_frequencies = data['itemDescription'].value_counts()
            st.subheader("Top 10 Most Frequent Items")
            fig, ax = plt.subplots(figsize=(10, 6))
            item_frequencies.head(10).plot(kind='bar', ax=ax)
            ax.set_title("Top 10 Most Frequent Items")
            ax.set_xlabel("Item Description")
            ax.set_ylabel("Frequency")
            ax.tick_params(axis='x', rotation=45)
            st.pyplot(fig)
            st.write("The bar graph above shows the top 10 most frequently purchased items in the dataset. These items are likely candidates for promotions or bundling.")

            # Visualization of Confidence vs Lift
            st.subheader("Confidence vs Lift for Association Rules")
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.scatterplot(x='confidence', y='lift', data=rules, ax=ax)
            ax.set_title("Confidence vs Lift for Association Rules")
            ax.set_xlabel("Confidence")
            ax.set_ylabel("Lift")
            st.pyplot(fig)
            st.write("The scatter plot above shows the relationship between confidence and lift for the association rules. Rules with higher confidence and lift indicate stronger associations between items.")

            # Recommendations based on the analysis
            st.subheader("Recommendations")
            st.write("""
                Based on the analysis, the following recommendations can be made:
                1. **Bundling Opportunities**: Items frequently purchased together (e.g., from frequent itemsets) can be bundled to encourage larger purchases.
                2. **Promotions**: Promote top-selling items or items with high lift to increase their sales further.
                3. **Product Placement**: Place items frequently purchased together closer in-store or online to facilitate easy selection.
                4. **Cross-Selling**: Use association rules to suggest complementary items during online or in-store shopping.
            """)

            # Conclusion
            st.subheader("Conclusion")
            st.write("""
                This analysis demonstrates the effectiveness of the Apriori algorithm for identifying patterns in transactional data.
                Key takeaways include:
                - Frequently purchased items provide insight into customer preferences.
                - Strong association rules highlight potential cross-selling and upselling opportunities.
                - Visualizations help businesses understand item relationships and transaction patterns clearly.
            """)

except FileNotFoundError:
    st.error(f"The file '{file_path}' was not found. Please ensure it is in the correct location.")
except Exception as e:
    st.error(f"An error occurred: {e}")
