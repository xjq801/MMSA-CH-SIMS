# Task46 创建与执行授权（P0/P1/P2/P3；hash-bound）

## 授权状态

- authorization_id: `USER-20260807-EXECUTE-SHARED-TASK46-PLAN`
- source: 用户明确要求定位共享对话中“好的，那你直接帮我拟定下一步的实验步骤吧，要尽可能详细，便于codex执行”后的回答，并直接执行；本地副本 `D:\桌面\任务安排.docx` SHA-256=`FE28A804C4656E0F57916256C3C84953AC21217945C6F2DA9BD3A5906920513E`
- route: IEEE T-AFFC CARM only
- anchor before this package: `origin/main@0aa8232f8c9586da36c3379ed5256c06a491e3ef`
- scope: 创建独立 Task46 执行线程并只执行 v1.25 P0→P1→P2→P3；P4 只有在全部冻结和自动门通过后一次性打开 `TRAIN_ROUTER_CONFIRM`，不得以本文件绕过门。
- forbidden: Task40 修复/重跑；Task45 修复/重跑；旧 DEV/DIAG_CONFIRM 复用；formal test；Task50；增加 seed；事后换指标/coverage/阈值；IJCV J0—J2/JH1—JH3/任务25/65。

## 前置条件

创建线程前必须把本文件、研究计划、预注册、target chain、failure tree、fair-baseline、access-boundary 与 machine-readable hashes 提交到 `origin/main`，并用独立 worktree 启动。任何 hash 不一致或 Task45 独立关闭审查缺失时，任务保持只读。

## 退出门

P0/P1/P2/P3 任何失败均停止并回交；P4 主 JSD 失败则关闭政策路线且 U4/U5 不执行。formal test 与 Task50 仍需另行用户授权，不能由本授权隐含。

