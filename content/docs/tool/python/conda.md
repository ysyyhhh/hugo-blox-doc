# conda

```shell
# 查看环境
conda env list

# 创建环境
conda create -n py3 python=3.6

# 通过yml文件创建环境
conda env create -f environment.yml

# 激活环境
conda activate py3

# 退出环境
conda deactivate

# 删除环境
conda remove -n py3 --all

```

## 迁移时可能会出现pip问题

可以在yml的pip:上面加上pip

```yml
name: py3
channels:
  - defaults
dependencies:
    - python=3.6
    - pip
    - pip:
        - -r requirements.txt
```
