# 1. 先导入 juliacall（用于 PySR）
import juliacall

# 2. 再导入 torch
import torch

# 3. 然后导入其他库
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

def main():
    print("=" * 50)
    print("环境测试报告")
    print("=" * 50)
    
    # 测试 PyTorch + CUDA
    print(f"\n✓ PyTorch 版本: {torch.__version__}")
    print(f"✓ CUDA 是否可用: {torch.cuda.is_available()}")
    
    if torch.cuda.is_available():
        print(f"✓ GPU 型号: {torch.cuda.get_device_name(0)}")
        print(f"✓ 显存总量: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB")
        
        # 简单的 GPU 计算测试
        x = torch.randn(1000, 1000).cuda()
        y = torch.mm(x, x.T)
        print(f"✓ GPU 计算测试通过（矩阵乘法 {y.shape}）")
    
    # 测试 NumPy + Pandas
    arr = np.array([1, 2, 3, 4, 5])
    df = pd.DataFrame({'a': arr})
    print(f"\n✓ NumPy 版本: {np.__version__}")
    print(f"✓ Pandas 版本: {pd.__version__}")
    
    # 测试 scikit-learn
    model = LinearRegression()
    print(f"✓ scikit-learn 导入成功")
    
    print("\n" + "=" * 50)
    print("✅ 所有测试通过！环境配置正确")
    print("=" * 50)

if __name__ == "__main__":
    main()