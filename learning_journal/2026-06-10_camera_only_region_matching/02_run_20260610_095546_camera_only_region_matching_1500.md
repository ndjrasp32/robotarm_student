# 2026-06-10 09:55:46 Camera-Only Region Matching Run / 카메라 전용 영역 매칭 학습

## Summary / 요약

- KR: Stage 1 9영역 학습을 카메라 추정 영역 기준으로 1500 iteration 다시 실행했고, 9개 영역 모두 마스터리 카운트를 채웠다.
- EN: Stage 1 9-region training was rerun for 1500 iterations using the camera-estimated region, and all 9 regions reached mastery counts.

## Run / 실행

| item | value |
| --- | --- |
| command / 명령 | `./scripts/train_coordinate_stage1_plane_128_500.sh` |
| run directory / 실행 경로 | `/home/spark-robotics/work/isaac/src/IsaacLab/logs/rsl_rl/mt4_coordinate_curriculum_direct/2026-06-10_09-55-46` |
| final checkpoint / 최종 checkpoint | `model_1499.pt` |
| training time / 학습 시간 | 1029.16 s |
| previous baseline / 이전 기준 | `experiments/20260610_031348_coordinate_region_mastery_1500_video.md` |

## Final Metrics / 최종 지표

| metric | value |
| --- | ---: |
| mean_reward | 6028.4316 |
| success_rate | 0.0005 |
| center_3cm_rate | 0.0005 |
| near_center_7cm_rate | 0.8667 |
| strict_region_center_success_rate | 0.0005 |
| mean_distance | 0.0555 m |
| camera_region_entry_rate | 0.9446 |
| camera_region_match_rate | 1.0000 |
| inside_workspace_rate | 0.8840 |
| target_stereo_visible_rate | 1.0000 |
| gripper_stereo_visible_rate | 0.9651 |
| mastered_region_count | 9 |

## Region Mastery / 영역 마스터리

| region | success count | mastered |
| ---: | ---: | ---: |
| 1 | 18 | 1 |
| 2 | 40 | 1 |
| 3 | 8 | 1 |
| 4 | 6 | 1 |
| 5 | 33 | 1 |
| 6 | 40 | 1 |
| 7 | 6 | 1 |
| 8 | 10 | 1 |
| 9 | 830 | 1 |

## Evidence / 근거 자료

- Source record / 원본 기록: [20260610_095546_camera_only_region_matching_1500.md](../../experiments/20260610_095546_camera_only_region_matching_1500.md)
- Plot directory / 그래프 경로: [20260610_095546_camera_only_region_matching_1500](../../logs/plots/20260610_095546_camera_only_region_matching_1500/)
- Demo video / 시연 영상: [20260610_074525_demo_9region_random_policy_2min_labeled.mp4](../videos/20260610_074525_demo_9region_random_policy_2min_labeled.mp4)
- Demo sequence / 시연 순서: [20260610_073944_demo_9region_random_policy_2min_sequence.csv](../videos/20260610_073944_demo_9region_random_policy_2min_sequence.csv)

## Interpretation / 해석

- KR: `camera_region_match_rate`가 1.0000이므로 현재 시뮬레이션의 카메라 영역 추정은 생성 영역과 일치했다.
- EN: Since `camera_region_match_rate` is 1.0000, the camera-estimated regions matched the generated regions in this simulation run.
- KR: 9개 영역 마스터리는 달성했지만, 마지막 batch 기준 strict 3cm 성공률은 낮다. 다음 학습은 영역 선택 이후 실제 타겟 중심으로 수렴하는 제어 안정성을 개선해야 한다.
- EN: All 9 region mastery counts were achieved, but the final-batch strict 3 cm success rate is low. The next training step should improve control stability after the region choice so the gripper converges to the true target center.

## Next Step / 다음 단계

- KR: 카메라 추정 영역을 유지하면서, 영역 내부 중심 접근 보상과 타겟 중심 3cm 수렴을 더 잘 연결한다.
- EN: Keep the camera-estimated region input, then better connect region-center approach reward with strict 3 cm convergence to the true target center.
