# chatgpt

![](https://img.shields.io/badge/language-python-blue.svg)
[![Forks](https://img.shields.io/github/forks/rosemary666/chatgpt)](https://img.shields.io/github/forks/rosemary666/chatgpt)
[![Stars](https://img.shields.io/github/stars/rosemary666/chatgpt)](https://img.shields.io/github/stars/rosemary666/chatgpt)
[![Contributors](https://img.shields.io/github/contributors/rosemary666/chatgpt)](https://github.com/rosemary666/chatgpt/graphs/contributors)
[![Docs](https://github.com/rosemary666/chatgpt/actions/workflows/deploy_doc.yaml/badge.svg)](https://github.com/rosemary666/chatgpt/actions/workflows/deploy_doc.yaml)
[![Pypi](https://github.com/rosemary666/chatgpt/actions/workflows/publish_pypi.yaml/badge.svg)](https://github.comrosemary666/chatgpt/actions/workflows/publish_pypi.yaml)
[![License: Apache2.0](https://img.shields.io/github/license/rosemary666/chatgpt)](https://github.com/rosemary666/chatgpt/blob/main/LICENSE)

[DOCS](https://rosemary666.github.io/chatgpt/)

chatgpt库的封装调用, 支持流式和非流式。

## 特性
- 支持流式和非流式
- 支持底层调用chatgpt的封装(很easy启动)
- 支持上层Http服务的封装调用(支持sse方式)

## 调用

### 安装
```shell
pip install py_chatgpt
```

### 底层调用 
- 非流式
```python
from py_chatgpt.core.chat_gpt_3 import ChatGptV3
cg = ChatGptV3(
    api_key="*****",
    system_prompt="请帮我把以下的工作内容填充为工作周报，用markdown格式以分点叙述的方式输出:",
)
answer = cg.chat_once("主要开展了三件事情, 第一是完成功能1的开发，第二是完成了xx的需求评审，第三是接待了xx客户")
print(answer)
cg.save_conversations("./conversations.json")
```

- 流式
```python
from py_chatgpt.core.chat_gpt_3 import ChatGptV3

cg = ChatGptV3(
    api_key="****" #请填写自己生成的api_key
)

streams = cg.chat_stream(prompt="**") #返回的流式结果
for stream in streams:
    print(stream)
```

### 上层调用
上层支持以sse的接口形式将结果返回给调用方，采用该方式可模拟chatgpt官方网页显示效果。

服务启动方式: 
```shell
1. cd python/py_chatgpt      
2. 修改conf/service.yaml配置文件(重点配置api_key和proxy)      
3. 执行run.sh即可启动   
```
     

### 接口文档
浏览器打开:
```shell
http://${ip}:${port}/api/v1/doc
```
即可在线访问(注意替换ip和port为真实启动的)