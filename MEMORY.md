# MEMORY.md - 长期记忆

## 少爷信息
- 称呼：少爷
- 主要用Windows工作，Chrome调试端口连着

---

## 股票数据 - 东方财富API

**涨停板/板块数据查询：**

```bash
# 东方财富涨停股API（不需要token，直接调）
curl -s "https://push2delay.eastmoney.com/api/qt/clist/get?pn=1&pz=100&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:0+t:6,m:0+t:80,m:1+t:2,m:1+t:23&fields=f2,f3,f4,f12,f14,f15,f16,f17,f18"
```

参数说明：
- `fs=m:0+t:6,m:0+t:80,m:1+t:2,m:1+t:23` = A股全市场（含主板/科创/创业/北交所）
- `fid=f3` = 按涨幅排序
- `f3>=9.9` 为涨停股
- 返回字段：f2=最新价, f3=涨幅%, f4=涨跌额, f12=代码, f14=名称

**查询今日板块涨跌幅：**
```bash
curl -s "https://push2delay.eastmoney.com/api/qt/clist/get?pn=1&pz=100&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:90+t:2&fields=f2,f3,f12,f14"
```

---

## Chrome调试连接

- Windows Chrome调试端口： `--remote-debugging-port=7777`
- 隧道已建立：本地 127.0.0.1:7777 → Windows
- 湖南人淘股吧博客：https://www.tgb.cn/blog/444409
- 3.21复盘文章ID未出，需要等

---

## 项目方向（少爷要做的）

### 当前重点：电竞数据平台（进行中）

**MVP目标：** 做一个能用的电竞数据站，3-4周跑通

**目标用户：** 电竞博彩/竞猜用户、竞猜平台、电竞爱好者

**第一版功能：**
1. 今日/明日比赛赛程
2. 比赛结果+比分
3. 战队排名
4. 历史对战记录
5. 赔率对比

**数据源（免费）：**
- DOTA2：OpenDota API（完全免费，无需key）
- CS2：Steam API + OpenDota
- LoL/Valorant：Riot API（免费注册）
- 赛事整合：PandaScore（有免费tier）
- 赔率：OddsPortal爬虫

**技术栈：**
- 后端：Python/FastAPI
- 数据库：PostgreSQL
- 前端：Vue3 or React
- 服务器：阿里云ECS 2核4G，约1500元/年

**开发步骤：**
- Day 1：打通 OpenDota API，跑通DOTA2数据
- Day 2-3：数据库设计 + 赛事赛程接口
- Day 4-5：战队排名+历史对战
- Day 6-7：前端展示页面
- 第2周：加上LoL/Valorant
- 第3周：赔率对比功能
- MVP完成：约3-4周

---

### 待后续扩展

**学术数据**（次推）
- 数据源：Semantic Scholar / CrossRef / arXiv / PubMed API（免费）
- 技术：Python + FastAPI + PostgreSQL + React
- 目标用户：科研人员、研究生、高校图书馆
- 预计MVP：2-4周
- 落地费用：约2000元/年

**招投标数据**（三推）
- 数据源：爬取100+政府招标网站
- 技术：Python爬虫 + Scrapy + Redis + RabbitMQ + ES
- 目标用户：企业销售/市场人员
- 预计MVP：2-3月
- 落地费用：约8000元（服务器+代理IP）

**手游数据**（练手）
- 数据源：App Store爬虫 + Google Play
- 技术：Python + FastAPI + PostgreSQL
- 差异化：玩家视角 + 开发者口碑 + AI评论总结

---

## Tushare token
- Token：6e07ab13440a8c77f75a081f102a339c22afc6c2ef0140c92a1c196e
- 状态：积分不够，暂不可用（需要2000+积分）

---

## 股票复盘方法（少爷提供）

### 一、数据整理
1. 梳理每日涨停票，按照题材板块进行分类
2. 梳理跌停票，找到市场的亏钱方向
3. 梳理连板梯队，按上涨高度和板块强度排序

### 二、盘面梳理
1. 整理昨日涨停的票今日表现，看是否有溢价
2. 整理出主流题材，确定板块状态：
   - 轮动板块有哪些，主流板块是哪些，支线板块有哪些，穿插板块又是哪些
   - 找到各板块龙头，确定个股在板块内的地位
   - 龙头为哪只票，是否有卡位地位，是否有不涨，跟风票是哪些
3. 确定资金偏向和方向：
   - 目前资金喜欢主板还是创业板
   - 喜欢沪深还是北证
   - 体量大的票还是体量小的票
4. 整理个人操作，总结今日操作是否完美，回顾盘中持仓心态

### 三、确定情绪
1. 确定盈亏效应：连板溢价率是否高，跌停大面数量如何
2. 确定板块情绪周期：启动、发酵、主升、高潮、退潮、冰点
3. 能够与新的消息面建立联系
4. 了解当日新闻及个股公告
5. 了解龙虎榜大佬操作方向
6. 思考大盘后续方向
7. 找到符合当下市场情绪的模式所对应的股票

### 四、明日计划
1. 分析手中个股明日该如何操作，只做应对不预判：
   - 超预期→持有
   - 符合预期→持仓
   - 不及预期→如何卖出
2. 筛选模式内的股票，符合预期的买入

---

## Word .doc 文件读取
- 使用 `olefile` + UTF-16-LE 解码可直接读取老版 .doc 文件内容
- python-docx 只支持 .docx（新格式），不支持 .doc（老格式）
- 示例代码：
  ole = olefile.OleFileIO(path)
  data = ole.openstream('WordDocument').read()
  text = data.decode('utf-16-le', errors='ignore')

## 技术笔记
- pip在WSL里没有权限安装，需要找其他方式
- 东方财富API用push2delay.eastmoney.com域名可以稳定访问
- 腾讯云SSH密码登录需修改/etc/ssh/sshd_config加PasswordAuthentication yes
- OpenCloudOS用yum不是apt-get
- PostgreSQL需要手动初始化：pg_ctl initdb -D /var/lib/pgsql/data

## Riot API账号
- 账号：XiaoYao24264
- 密码：HAOyan123.
- API Key：RGAPI-469b9f4b-66e9-4b12-afef-7a5bd1705cf4
- Key有效，已测试可用（br1.api可用）
- 申请地址：https://developer.riotgames.com/
