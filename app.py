import streamlit as st
import psutil
from file_handler import parse_uploaded_file, save_results_to_file
from tko_algorithm.tko_basic import AlgoTKOBasic
from tku_algorithm.AlgoTKU import AlgoTKU  # Đảm bảo rằng bạn đã có lớp AlgoTKU
print(type(AlgoTKU))

# Title with custom style
st.title("High Utility Itemset Mining with TKO-TKU Algorithm")

def read_result():
    # Đọc file output.txt và xử lý nội dung
    file_name = "./data/output.txt"
    try:
        with open(file_name, "r", encoding="utf-8") as file:
            lines = file.readlines()

        results = []
        for idx, line in enumerate(lines):
            itemset, util = line.split("#UTIL:")
            items = sorted(map(int, itemset.split()))  
            formatted_itemset = ", ".join(map(str, items))  
            results.append(f"Itemset {idx + 1}: {formatted_itemset} #UTIL: {util.strip()}")

        st.subheader("Kết quả đã xử lý:")
        for result in results:
            st.text(result)

    except FileNotFoundError:
        st.error(f"File '{file_name}' không tồn tại. Vui lòng kiểm tra lại.")
    except Exception as e:
        st.error(f"Có lỗi xảy ra: {e}")

def print_status(totalTime, memory_before, memory_after, k_itemsets):
    st.subheader("Algorithm Statistics")
    st.markdown(f"""
                - **Execution Time:** {totalTime:.2f} seconds
                - **Memory Usage Before:** {memory_before:.2f} MB
                - **Memory Usage After:** {memory_after:.2f} MB
                - **Total High-Utility Itemsets Found:** {k_itemsets}
            """)

def download_button(file_path="./data/output.txt"):
    try:
        with open(file_path, "rb") as file:  
            st.download_button(
                label="Tải xuống file",
                data=file,  
                file_name=file_path.split("/")[-1], 
                mime="text/plain",  
            )

    except FileNotFoundError:
        st.error(f"File '{file_path}' không tồn tại. Vui lòng kiểm tra lại.")
    except Exception as e:
        st.error(f"Có lỗi xảy ra: {e}")
with st.sidebar:
    st.header("Input Parameters")
    uploaded_file = st.file_uploader("Upload Dataset", type=["txt"], label_visibility="collapsed")
    k = st.number_input("Select Top-K Value", min_value=1, value=3)
    algorithm = st.selectbox("Select Algorithm", ["TKO", "TKU"])

run_button = st.button("Run", use_container_width=True)

if run_button:
    if uploaded_file is not None:
        run_status = 1
        content = uploaded_file.read().decode("utf-8")
        lines = content.splitlines()  # Tách nội dung thành từng dòng
        normalized_content = "\n".join(lines)  # Ghép lại các dòng đúng chuẩn
        
        input_file_path = "./data/uploaded_dataset.txt"
        output_file_path = "./data/output.txt"
        with open(input_file_path, "w", encoding="utf-8") as f:
            f.write(normalized_content)
        
        process = psutil.Process()
        memory_before = process.memory_info().rss / (1024 * 1024)  # Convert to MB

        if algorithm == "TKO":
            # Run TKO Algorithm
            algo_tko = AlgoTKOBasic()
            algo_tko.run_algorithm(input_file_path, k)
            memory_after = process.memory_info().rss / (1024 * 1024)  # Convert to MB
            k_itemsets = []
            while not algo_tko.k_itemsets.empty():
                itemset = algo_tko.k_itemsets.get()
                k_itemsets.append((itemset.prefix + [itemset.item], itemset.utility))

            save_results_to_file(output_file_path, k_itemsets)

            st.success("TKO Algorithm completed successfully!", icon="✅")
            st.markdown(f"Results saved to **`{output_file_path}`**:")
            totalTime = algo_tko.total_time
            k_itemsets = len(k_itemsets)  
        elif algorithm == "TKU":
            algo_tku = AlgoTKU()
            algo_tku.runAlgorithm(input_file_path, output_file_path, k)
            memory_after = process.memory_info().rss / (1024 * 1024)  # Convert to MB
            st.success("TKU Algorithm completed successfully!", icon="✅")
            st.markdown(f"Results saved to **`data/output.txt`**:")
            totalTime = algo_tku.totalTime
            k_itemsets = algo_tku.patternCount
        else:
            st.warning("Algorithm selection is not recognized.", icon="⚠️")
    else:
        st.error("Please upload a dataset file before running.", icon="🚨")
    
    read_result()
    print_status(totalTime, memory_before, memory_after, k_itemsets)
    download_button()
# Footer Section
st.markdown("---")
