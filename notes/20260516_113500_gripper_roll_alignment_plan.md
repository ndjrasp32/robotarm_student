# 20260516_113500 gripper roll alignment plan

## Teacher Observation

- GUI play 확인 결과, 집게가 빨간 구체 근처까지는 잘 접근하지만 한쪽 집게 다리가 치우쳐진 상태로 접근을 멈춘다.
- 최종 목적은 빨간 구체를 두 집게 다리 사이 중앙에 끼우는 것이므로, 집게의 roll 방향 정렬이 필요하다.

## Diagnosis

### 그리퍼 기하 구조

`gripper_link` 형상 (`create_mt4_simplified_v3_gripper_axis.py` 기준):

| 파트 | 로컬 위치 |
|------|-----------|
| `left_finger` | (0.120, **+0.034**, 0.0) |
| `right_finger` | (0.120, **-0.034**, 0.0) |
| `left_pad` | (0.158, **+0.034**, 0.0) |
| `right_pad` | (0.158, **-0.034**, 0.0) |
| `gripper_center_offset_b` | (0.158, 0.0, 0.0) |

두 손가락은 **그리퍼 로컬 Y축** 방향으로 고정 간격으로 벌어져 있다. `gripper_pitch` 관절은 Y축 기준으로 그리퍼 전체를 회전시킨다.

### 현재 reward 누락 요소

| 체크 항목 | 현재 reward | 상태 |
|-----------|-------------|------|
| 그리퍼 중심이 타깃에 가까워지는가 | `distance` | ✅ |
| 그리퍼 +X축이 접근 방향과 일치하는가 | `insertion_alignment` | ✅ |
| 손가락 벌어진 방향(+Y축)이 올바른가 | 없음 | ❌ |

현재 observation은 `gripper_forward`(+X 방향, 3값)만 포함하며, 그리퍼가 접근 방향 기준으로 얼마나 roll되어 있는지 알 수 없다. reward도 roll을 제어하는 신호가 없어, 정책은 손가락이 어느 방향으로 벌어져 있든 무관하게 학습된다.

## Codex Proposal

### 1. Observation 추가 (28 → 31)

그리퍼 로컬 +Y축을 월드 좌표로 변환한 `gripper_side`(3값)를 observation에 추가한다. 이를 통해 정책이 손가락 벌어진 방향을 직접 인식할 수 있다.

### 2. Reward 추가: `gripper_roll_alignment_weight`

손가락이 올바르게 벌어지려면, 그리퍼 Y축이 접근 방향과 수직인 평면에서 최대한 world-up(Z)에 가까워야 한다(손가락이 위아래로 벌어져 타깃을 좌우가 아닌 중앙에서 잡도록).

계산 방법:
1. `world_up = [0, 0, 1]`을 접근 방향(`approach_dir`) 성분 제거 후 정규화 → `up_perp`
2. `gripper_roll_alignment = dot(gripper_side, up_perp)` → [-1, 1] 범위
3. `gripper_roll_reward = clamp(0.5 * (alignment + 1), 0, 1)` → [0, 1] 범위
4. stage1 수준에서 ungated 적용, weight는 env var `MT4_REACH_GRIPPER_ROLL_WEIGHT`로 제어

기본값: `gripper_roll_alignment_weight = 0.0` (통합 모드 비활성), stage4_center 기본 `2.5`

### 변경 파일

- `source/mt4_reach_direct/mt4_reach_env.py`
  - `observation_space`: 28 → 31
  - `gripper_side_axis_b = (0.0, 1.0, 0.0)` cfg 추가
  - `gripper_roll_alignment_weight = 0.0` cfg 추가
  - `__init__`: `self.gripper_side`, `self.gripper_roll_alignment` 텐서 추가
  - `_compute_intermediate_values`: gripper_side 및 roll_alignment 계산 추가
  - `_get_observations`: `gripper_side` obs 추가
  - `_get_rewards`: `gripper_roll_reward` 항 추가
  - `_get_dones` log: `mean_gripper_roll_alignment` 추가
  - `_apply_training_mode_cfg` stage4_center: env var 기본값 `2.5` 설정

- `scripts/train_stage4_relaxed_gate_128_300.sh`
  - `MT4_REACH_GRIPPER_ROLL_WEIGHT` 추가

## Expected Effect

- 정책이 observation을 통해 손가락 방향을 인식하고, reward 신호를 통해 손가락이 위아래로 벌어지도록 학습
- `mean_gripper_roll_alignment`가 1.0에 가까워지면 손가락이 올바르게 정렬된 것
- 성공률 직접 향상보다는 최종 삽입 품질(gripper center precision) 개선이 주목적
