# 20260515_155255 blue shell exponential reward plan

## Teacher Idea

- 마지막 파란 구체가 빨간 구체 중심과 같다면, 그 지점에 집게 중심이 들어갔을 때 성공으로 보는 것이 자연스럽다.
- 파란 guide를 부채꼴 보상으로만 두면, 같은 거리권에서 맴돌며 보상을 반복해서 받을 수 있다.
- 같은 거리권의 보상은 한 번만 받고, 다음으로 더 가까운 거리권에 들어갈 때 새 보상을 받도록 만들면 중심 방향으로 계속 진행할 가능성이 높다.
- 멀리서 가까워질 때 보상은 선형보다 지수형이 좋을 수 있다. 가까운 곳에서 더 민감한 보상을 주기 때문이다.
- 학습된 checkpoint 하나를 시연용으로 바로 볼 수 있는 스크립트가 필요하다.

## Codex Interpretation

현재 `moving_pregrasp_final_rate`는 마지막 파란 marker가 표시되는 단계에 도달했다는 뜻에 가깝다. 즉, "마지막 파란 구체가 현재 빨간 중심에 있다"는 의미이지, "집게 중심이 그 마지막 파란 구체 중심에 정확히 들어갔다"는 뜻은 아니다.

그래서 이번 변경은 두 가지를 분리한다.

- `moving_pregrasp_final_rate`: 마지막 파란 marker 단계까지 진행됨
- `blue_final_center_ready_rate`: 마지막 파란 marker, 즉 빨간 중심에 집게 중심이 실제로 들어감

`goal=center` 모드에서 `blue_final_center_ready_rate`가 참이면 성공 판정에도 포함한다. 이때 정렬, lateral error, target clearance 조건은 유지한다.

## Reward Change

파란 guide 보상에 다음 요소를 추가했다.

- exponential center reward:
  - `exp(-(pregrasp_distance / exp_scale)^2)`
  - 파란 중심에 가까워질수록 급격히 커진다.
- one-shot shell reward:
  - `pregrasp_distance`를 일정 shell size로 나눈다.
  - 한 episode와 한 moving-guide 단계 안에서 이미 얻은 거리 shell은 다시 보상하지 않는다.
  - 더 가까운 shell에 처음 들어갈 때만 보상을 준다.
  - 파란 marker가 다음 단계로 이동하면 shell 기록을 초기화한다.

## Added Parameters

- `MT4_REACH_MOVING_PREGRASP_EXP_WEIGHT`
- `MT4_REACH_MOVING_PREGRASP_SHELL_WEIGHT`
- `MT4_REACH_MOVING_PREGRASP_SHELL_SIZE`
- `MT4_REACH_MOVING_PREGRASP_EXP_SCALE`

## Added Metrics

- `mt4/blue_final_center_ready_rate`
- `mt4/mean_moving_pregrasp_exp_reward`
- `mt4/mean_moving_pregrasp_shell_improvement`
- `mt4/mean_best_moving_pregrasp_distance`

## Demo Script

새 시연 스크립트:

```bash
~/work/robotarm/mt4_isaac_lab_task/scripts/play_blue_funnel_demo.sh
```

특징:

- `best_checkpoint.txt`에 기록된 checkpoint를 사용한다.
- 빨간 목표는 task reset 때마다 랜덤 생성된다.
- 파란 guide는 center mode로 빨간 중심까지 이동한다.
- GUI/VNC 시연을 위해 `DISPLAY=:1`을 사용한다.
- 기본 90초만 실행하고, `DEMO_SECONDS=0`이면 사용자가 닫을 때까지 실행한다.

## Expected Next Test

다음 학습은 기존 broad funnel curriculum을 다시 실행하되, 새 shell/exponential reward가 켜진 상태로 진행한다.

```bash
~/work/robotarm/mt4_isaac_lab_task/scripts/train_stage4_blue_funnel_128_800.sh --seed 42
```

관찰할 핵심 지표:

- `blue_final_center_ready_rate`
- `moving_pregrasp_step_ready_rate`
- `moving_pregrasp_final_rate`
- `mean_moving_pregrasp_shell_improvement`
- `mean_moving_pregrasp_exp_reward`
- `stage4_center_ready_rate`
- `success_rate`
