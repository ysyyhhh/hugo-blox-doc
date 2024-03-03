
# poetry

## poetry 出现的错误及解决方法

### poetry install 时Failed to create the collection: Prompt dismissed

解决方案: 关闭keyring

```shell
python3 -m keyring --disable
```

原因:
[https://github.com/python-poetry/poetry/issues/1917](https://github.com/python-poetry/poetry/issues/1917)
