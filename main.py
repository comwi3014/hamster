import keyboard
import time
from roboid import HamsterS, wait

def main():
    print("햄스터 로봇 연결을 시작합니다. 동글이 꽂혀있고 로봇 전원이 켜져 있는지 확인해 주세요.")
    hamster = HamsterS()
    print("연결 성공! 키보드 방향키(↑, ↓, ←, →)로 로봇을 조작할 수 있습니다.")
    print("'+' 또는 '=' 키로 속도를 올리고, '-' 키로 속도를 줄일 수 있습니다.")
    print("스페이스(Space) 키를 누르면 '삑' 소리가 납니다.")
    print("종료하려면 'q' 키 또는 'Ctrl+C'를 누르세요.")

    # 기본 이동 속도 설정 (0~100 범위, 30이 기본값)
    speed = 30
    last_speed_change_time = 0
    cooldown = 0.2  # 속도 조절 쿨다운 (초)
    space_pressed = False  # 스페이스 키 눌림 상태 플래그 (한 번만 울리게 방지)

    try:
        while True:
            # 'q' 키가 눌리면 프로그램 종료
            if keyboard.is_pressed("q"):
                print("조작을 종료합니다.")
                break

            # 속도 조절 키 감지 (+ / = 키로 올림, - 키로 내림)
            current_time = time.time()
            if current_time - last_speed_change_time > cooldown:
                if keyboard.is_pressed("+") or keyboard.is_pressed("="):
                    speed = min(100, speed + 5)
                    print(f"속도 증가: {speed}")
                    last_speed_change_time = current_time
                elif keyboard.is_pressed("-"):
                    speed = max(10, speed - 5)
                    print(f"속도 감소: {speed}")
                    last_speed_change_time = current_time

            # 스페이스 키 감지 (삑 소리 재생)
            if keyboard.is_pressed("space"):
                if not space_pressed:
                    hamster.note("C5", 0.15)  # 5옥타브 도 음을 0.15초 동안 출력
                    print("Beep!")
                    space_pressed = True
            else:
                space_pressed = False

            # 방향키 입력 감지 및 모터 제어
            if keyboard.is_pressed("up"):
                hamster.wheels(speed, speed)  # 전진
            elif keyboard.is_pressed("down"):
                hamster.wheels(-speed, -speed)  # 후진
            elif keyboard.is_pressed("left"):
                hamster.wheels(-speed, speed)  # 제자리 좌회전
            elif keyboard.is_pressed("right"):
                hamster.wheels(speed, -speed)  # 제자리 우회전
            else:
                hamster.wheels(0, 0)  # 정지

            wait(20)  # CPU 사용량을 줄이고 반응 속도를 유지하기 위해 20ms 대기
            
    except KeyboardInterrupt:
        print("프로그램이 강제 종료되었습니다.")
    finally:
        # 종료 시 로봇 정지 및 소리 끄기
        hamster.wheels(0, 0)
        hamster.note(0)
        print("로봇이 정지되었습니다.")

if __name__ == "__main__":
    main()
