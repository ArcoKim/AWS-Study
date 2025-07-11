import boto3
import json
import random
from datetime import datetime
import time

# Kinesis 설정
stream_name = "input-stream"
region_name = "ap-northeast-2"

# Kinesis 클라이언트 생성
kinesis = boto3.client("kinesis", region_name=region_name)

# 랜덤 레벨과 경로
levels = ["info", "warn", "error"]
paths = ["/user/login", "/user/logout", "/api/search", "/admin/create"]

def generate_event(i):
    now = datetime.now()
    event = {
        "id": i % 100,  # 0~99로 제한해서 파티션 효과 확인
        "level": random.choice(levels),
        "path": random.choice(paths),
        "status": random.choice([200, 201, 400, 403, 500]),
        "event_time": now.isoformat(timespec='seconds')  # ISO-8601 형식
    }
    return event

# 데이터 삽입 루프
record_count = 50000  # 총 보낼 메시지 수
batch_size = 100       # Kinesis는 한번에 최대 500개까지 가능

for i in range(0, record_count, batch_size):
    batch = []
    for j in range(batch_size):
        event = generate_event(i + j)
        data = {
            'Data': json.dumps(event),
            'PartitionKey': str(event["id"])
        }
        batch.append(data)

    response = kinesis.put_records(Records=batch, StreamName=stream_name)

    print(f"Inserted {i + batch_size} records")
    time.sleep(0.5)  # 너무 빠르게 보내면 제한에 걸릴 수 있음
