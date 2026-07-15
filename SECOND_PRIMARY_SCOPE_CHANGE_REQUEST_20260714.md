# 第二人工主集范围变更请求：LAI-GAI图像跨域路径

> 日期：2026-07-14  
> 发起任务：10-M1–M2 数据与协议  
> 用户决定：`APPROVED_PATH_1`  
> 总控状态：`APPROVED_SC-20260714-01_AND_AUTHORIZED_METADATA_READONLY`
> 执行结果：`NO_GO_PENDING_ASSET_METADATA`；详见`M1_LAI_GAI_OSF_METADATA_AUDIT_20260714.md`

## 1. 请求内容

将当前执行材料中的“第二人工多模态主集”降级为“第二人工跨域图像主集/缺失模态验证集”，候选固定为LAI-GAI v05。该变更只调整第二主集模态与论文可声称的泛化范围，不改变以下冻结项：

- 构念：`public-induced audience affect`；
- 真值：独立人类诱发反应，必须为`HUMAN_GOLD`；
- T0：只使用发布/呈现时内容，不使用目标反应或未来互动；
- 主指标：Jensen–Shannon divergence；
- 银标边界：生成prompt、目标生成类别和模型标签不得替代人类响应真值；
- 任务20门：G1/G2未书面通过前不得创建。

## 2. 证据基础

- LAI-GAI官方论文v05报告847张AI生成图像、六项研究、N=2470、58个国家；测量图像实际诱发的主观反应。
- 论文声明OSF发布所有图像的raw data、均值和标准差，理论上可按图像构造经验反应分布。
- 847张中仅544张的最高人类评分与预设目标情感一致，证明生成prompt/目标类别不能当真值。
- 稳定入口：项目`10.17605/OSF.IO/V8DKM`、分析数据`10.17605/OSF.IO/8P572`、图像`10.17605/OSF.IO/K8XVH`。

## 3. 请求00批准的下一动作

仅批准公开元数据只读审计：

1. 核三个OSF组件的逐资产license与license locator；
2. 核version/revision、last modified、file tree、文件名、字节数和公开hash；
3. 核是否gated、是否需要账户、是否允许非商业学术使用及派生发布；
4. 核raw data字段是否能构造逐图经验分布，核图像ID/group和prompt泄漏边界。

00最终授权只覆盖无需登录的网页可见元数据，不包含raw data字段读取、标签映射或split构建。已在该窄化边界内执行；网页未显示的逐资产字段均保留为`UNKNOWN`。

当前不请求、也不授权：

- 下载图像ZIP或raw data包；
- 调用API、付费服务或登录态；
- 修改G1/G2为通过；
- 生成正式split、启动训练或创建任务20。

若网页元数据不足，任务10将在下载任何小型公开元数据文件前，先回报文件名、预计大小、许可和用途并重新申请。

## 4. 论文主张降级

批准后论文最多声称“一个社交视频主集 + 一个跨域图像人工主集上的受众诱发分布预测/缺失模态验证”，不得声称两个多模态视频主集，也不得把跨模态结果写成同域复现。

## 5. 当前门状态

- 第二主集：`USER_SELECTED_LAI_GAI_PENDING_ASSET_AUDIT_AND_00_FREEZE`
- G1：`BLOCKED_SECOND_PRIMARY_NOT_YET_FROZEN`
- G2：`NOT_ELIGIBLE_G1_BLOCKED`
- `formal_split=false`
- 任务20：`PROHIBITED`

## 6. 00书面处理结果

- 范围变更已由00以`SC-20260714-01`批准并写入总纲v1.6。
- 只读元数据审计已由`AUTH-00-LAI-GAI-OSF-META-RO-20260714`授权；完整边界见`TASK00_LAI_GAI_SCOPE_AND_AUDIT_AUTHORIZATION_20260714.md`。
- 本批准只冻结数据角色方向，不冻结LAI-GAI资产，不通过G1/G2，也不授权下载、API、训练、正式split或任务20。
