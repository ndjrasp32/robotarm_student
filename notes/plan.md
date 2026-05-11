# MT4 Simplified Reach - Isaac Lab Direct RL

## 목적

MT4 simplified v2 모델을 사용하여 Isaac Lab Direct RL 환경을 만든다.

## v0 Task

- Reach task
- 4DOF arm
- gripper 제외
- camera 제외
- target position은 Isaac 내부 좌표로 제공

## Action

- base_yaw target delta
- shoulder target delta
- elbow target delta
- wrist_pitch target delta

## Observation

- joint positions
- joint velocities
- end-effector position
- target position
- target - end-effector vector

## Reward

- distance 감소 보상
- 목표점 근접 보상
- success bonus
- time penalty

## 이후 확장

1. 병렬 env 수 증가
2. policy play 영상 녹화
3. pick pre-grasp task
4. rule-based gripper
5. camera perception 연결
