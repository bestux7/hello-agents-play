""" 使用BFCL数据集 """

from hello_agents.evaluation import BFCLDataset

dataset = BFCLDataset(
    bfcl_data_dir="./temp_gorilla/berkeley-function-call-leaderboard/bfcl_eval/data",
    category="simple_python"
)

data = dataset.load()

print(f"✅ 加载了 {len(data)} 个测试样本")
print(f"✅ 加载了 {len(dataset.ground_truth)} 个ground truth")

categories = dataset.get_available_categories()
print(f"支持的类别: {categories}")

